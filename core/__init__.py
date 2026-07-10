"""Core — 跨平台通用爬虫库"""
from .config import Config
from .scraper import BaseScraper
from .reviews import ReviewExtractor
from .filter import FakeReviewFilter
from .ai_vision import AIVision
from .popup import PopupDetector
