"""配置管理 — 跨平台通用"""
import json, os, sys
from pathlib import Path

# 探测运行平台
IS_MAC = sys.platform == 'darwin'
IS_WIN = sys.platform == 'win32'

class Config:
    """全局配置，按优先级: 环境变量 > api_keys.json > 默认值"""

    _instance = None

    def __init__(self):
        repo_root = Path(__file__).resolve().parents[1]
        self.config_dir = repo_root / 'config'
        self.data_dir = repo_root / 'data'

        # 加载 API 密钥
        self.api_keys = self._load_json('api_keys.json')
        self.proxy_config = self._load_json('proxy.json')
        self.settings = self._load_json('settings.json', include_defaults=True)

        # CDP端口
        self.cdp_port = self.settings.get('cdp_port', 9223 if IS_MAC else 9222)

        # 平台特定路径
        if IS_MAC:
            self.chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            self.user_data_dir = '/tmp/taobao-scrape'
        else:
            self.chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            self.user_data_dir = os.path.expanduser(r'~\AppData\Local\taobao-scrape')

        # 代理
        self.proxy = self.proxy_config.get('default', {})
        self.proxy_mode = self.settings.get('proxy_mode', 0)

        # Bark
        self.bark_url = self.api_keys.get('bark', {}).get('url', '')

    def _load_json(self, filename, include_defaults=False):
        path = self.config_dir / filename
        if not path.exists():
            path = self.config_dir / f'{filename}.example'
        if path.exists():
            with open(path, encoding='utf-8') as f:
                return json.load(f)
        return {} if not include_defaults else self._default_settings()

    def _default_settings(self):
        return {
            'cdp_port': 9223 if IS_MAC else 9222,
            'proxy_mode': 1,
            'max_minutes': 30,
            'min_reviews': 3,
            'delay_min': 3, 'delay_max': 8,
            'page_timeout': 180,
        }

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# 全局单例
cfg = Config
