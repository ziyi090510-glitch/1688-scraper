"""结果存储 — 按平台分文件夹，自动创建二级分类"""
import json, os, shutil
from pathlib import Path
from datetime import datetime

PLATFORMS = ['taobao', '1688', 'xiaohongshu', 'douyin']

class Storage:
    """数据存储管理"""

    def __init__(self, data_root=None):
        if data_root is None:
            data_root = Path(__file__).resolve().parents[1] / 'data'
        self.root = Path(data_root)
        self._ensure_dirs()

    def _ensure_dirs(self):
        for p in PLATFORMS:
            (self.root / p).mkdir(parents=True, exist_ok=True)
            (self.root / p / 'images').mkdir(exist_ok=True)
            (self.root / p / 'reports').mkdir(exist_ok=True)

    def save_results(self, platform, data, category=None):
        """保存爬取结果
        Args:
            platform: taobao/1688/xiaohongshu/douyin
            data: dict with qualified/unqualified
            category: 二级分类(如'手机壳/定制'), 自动创建子目录
        """
        base = self.root / platform
        if category:
            base = base / category
            base.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = base / f'results_{ts}.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                'platform': platform,
                'category': category,
                'timestamp': ts,
                **data
            }, f, ensure_ascii=False, indent=2)
        return path

    def save_image(self, platform, category, filename, data):
        """保存图片到对应分类目录"""
        base = self.root / platform / 'images'
        if category:
            base = base / category
            base.mkdir(parents=True, exist_ok=True)
        path = base / filename
        with open(path, 'wb') as f:
            f.write(data)
        return path

    @classmethod
    def list_platforms(cls):
        return PLATFORMS
