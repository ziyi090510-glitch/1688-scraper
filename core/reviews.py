"""评价提取器 — 支持淘宝(滚动)和1688(Drawer+分页)"""
import time, re, json
from .filter import FakeReviewFilter

class ReviewExtractor:
    """评价提取 — 自动识别平台"""

    def __init__(self, page):
        self.page = page
        self.filter = FakeReviewFilter()

    def extract_taobao(self, max_reviews=200):
        """淘宝: 点击查看全部 → 滚轮逐段加载"""
        try:
            self.page.locator('[class*="footer"]').filter(has_text='查看全部评价').click(timeout=3000)
        except:
            return []
        time.sleep(3)

        prev = 0
        for step in range(50):
            self.page.mouse.wheel(0, 800)
            time.sleep(0.8)
            current = self.page.evaluate("document.querySelectorAll('[class*=\"Comment\"]').length")
            if current == prev and step > 8:
                break
            if current >= 250:
                break
            prev = current

        return self._parse_taobao_comments()[:max_reviews]

    def extract_1688(self, max_reviews=200):
        """1688: 打开Drawer → 翻页"""
        try:
            self.page.locator('.evaluation-more .ant-btn').first.click(timeout=3000)
        except:
            return []
        time.sleep(3)

        total_pages = self.page.evaluate("""() => {
            let max = 1;
            document.querySelectorAll('.ant-pagination-item').forEach(el => {
                let n = parseInt(el.textContent);
                if (!isNaN(n) && n > max) max = n;
            });
            return max;
        }""")

        all_reviews = []
        for page in range(1, min(total_pages + 1, 11)):
            self.page.evaluate(f"document.querySelector('.ant-pagination-item-{page}')?.click()")
            time.sleep(1.5)
            reviews = self._parse_1688_comments()
            all_reviews.extend(reviews)

        return all_reviews[:max_reviews]

    def _parse_taobao_comments(self):
        return self.page.evaluate("""() => {
            const comments = document.querySelectorAll('[class*="Comment"]');
            const result = [];
            const seen = new Set();
            comments.forEach(el => {
                let t = (el.textContent || '').trim();
                if (t.length < 30) return;
                if (t.match(/^[\\u4e00-\\u9fa5]+\\d+[\\u4e00-\\u9fa5]+\\d+/)) return;
                const key = t.slice(0, 60);
                if (seen.has(key)) return;
                seen.add(key);
                t = t.replace(/近\\d+个月好评率高达[\\d.]+%/g, '');
                t = t.replace(/用户评价[·\\s]*[\\d万+]+/g, '');
                t = t.replace(/商家回复[：:].*$/gm, '');
                const m1 = t.match(/^(.+?)(\\d{4}-\\d{2}-\\d{2})已购[：:](.+?)收到了[，,]?(.*)/);
                if (m1) {
                    const user = m1[1].trim();
                    if (user.length > 8 && /\\d/.test(user)) return;
                    result.push({user: user.slice(0,20), date: m1[2], text: m1[4].trim().slice(0, 150)});
                    return;
                }
                const m2 = t.match(/^(.+?)(\\d{4}年\\d{1,2}月\\d{1,2}日)已购[：:](.+)/);
                if (m2) {
                    const user = m2[1].trim();
                    if (user.length > 8 && /\\d/.test(user)) return;
                    const rest = m2[3].trim();
                    const idx = rest.indexOf('收到了');
                    const txt = (idx >= 0 ? rest.slice(idx+3).replace(/^[，,]/,'') : rest).trim().slice(0, 150);
                    result.push({user: user.slice(0,20), date: m2[2], text: txt});
                }
            });
            return result;
        }""")

    def _parse_1688_comments(self):
        return self.page.evaluate("""() => {
            var body = document.querySelector('.ant-drawer-body');
            if (!body) return [];
            var text = body.textContent.trim();
            var parts = text.split(/已购[：:]/);
            var reviews = [];
            for (var i = 1; i < parts.length; i++) {
                var p = parts[i].trim();
                var m = p.match(/^(\\d+)\\s*个?\\s*(.*)/);
                var qty = m ? m[1] : '?';
                var rest = (m ? m[2] : p).slice(0, 300);
                var prevEnd = parts[i-1].trim();
                var userMatch = prevEnd.match(/([\\u4e00-\\u9fa5\\*a-zA-Z0-9]{2,15}|匿名购买)\\s*(\\d+)天前$/);
                var user = userMatch ? userMatch[1] : '?';
                var days = userMatch ? userMatch[2] : '?';
                reviews.push({user: user, days: days, qty: qty, text: rest});
            }
            return reviews;
        }""")

    def filter_fake(self, reviews):
        """过滤刷单评论"""
        return self.filter.filter_all(reviews)
