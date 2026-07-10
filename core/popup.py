"""弹窗检测 — 5维覆盖（淘宝/1688通用）"""
class PopupDetector:
    """弹窗检测器"""

    def detect(self, page):
        """全量检测"""
        try:
            txt = page.content().lower()
            for k in ['操作频繁','验证码','拖动滑块','安全验证','人机验证','请稍后再试']:
                if k in txt:
                    return True
            return self.quick_detect(page)
        except:
            return False

    def quick_detect(self, page):
        """轻量检测(不加载content)"""
        try:
            return page.evaluate("""() => {
                if (document.querySelector('#nc_1_n1z, .nc_wrapper, [id*="nc_"], .slidetounlock')) return 1;
                if (document.querySelector('[class*="captcha"], [class*="verify"]')) return 1;
                let divs = document.querySelectorAll('body > div');
                for (let d of divs) {
                    let s = window.getComputedStyle(d);
                    let z = parseInt(s.zIndex) || 0;
                    let r = d.getBoundingClientRect();
                    if (z > 900 && s.position === 'fixed' && r.width > 250 && r.height > 150) return 2;
                }
                if (window.location.href.match(/verify|captcha|login/i)) return 3;
                return 0;
            }""") > 0
        except:
            return False
