"""核心爬取引擎 — 跨平台通用"""
import time, random, re, json, sys
from urllib.parse import quote
from pathlib import Path
from .popup import PopupDetector
from .config import cfg as Cfg

class BaseScraper:
    """爬虫基类 — 封装CDP连接、搜索、详情页爬取"""

    def __init__(self, browser, platform='unknown'):
        self.browser = browser
        self.platform = platform
        self.popup = PopupDetector()
        self._cfg = Cfg.get()
        self.start_time = time.time()
        self.results = {'qualified': [], 'unqualified': []}

    def gbk_encode(self, text):
        """GBK编码关键词（1688需要）"""
        return quote(text.encode('gbk'))

    def save_results(self):
        """保存结果到 data/{platform}/ 目录"""
        cfg = Cfg.get()
        data_dir = cfg.data_dir / self.platform
        data_dir.mkdir(parents=True, exist_ok=True)
        path = data_dir / 'results.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                'platform': self.platform,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'qualified_count': len(self.results['qualified']),
                'unqualified_count': len(self.results['unqualified']),
                'qualified': self.results['qualified'],
                'unqualified': self.results['unqualified'],
            }, f, ensure_ascii=False, indent=2)
        return path

    def elapsed(self):
        return (time.time() - self.start_time) / 60

    def wait_popup(self, page):
        """弹窗等待 — 手动处理"""
        print('\n⚠️ 弹窗！等待手动处理...')
        for n in range(180):
            time.sleep(10)
            if not self.popup.detect(page):
                print(f'✅ 已解除 ({(n+1)*10}s)')
                time.sleep(random.randint(8, 15))
                return True
        return False

    def pre_check(self, page):
        """每个操作前的弹窗预检"""
        if self.popup.quick_detect(page):
            return self.wait_popup(page)
        return True
