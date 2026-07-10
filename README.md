# 1688-Scraper — 多平台电商爬虫共享库

## 结构
```
core/           ← 跨平台通用（Mac/Win 共享）
  scraper.py      核心爬取引擎
  reviews.py      评价提取（淘宝滚动 + 1688 Drawer分页）
  filter.py       刷单过滤
  ai_vision.py    图片识别（SiliconFlow）
  popup.py        弹窗检测（5维）
  config.py       全局配置

platforms/       ← 平台特定（分 Mac/Win）
  mac/browser.py  Chrome启动（Mac）
  windows/browser.py Chrome启动（Win）

database/        ← 结果存储
  storage.py      按平台分目录 + 二级分类

config/          ← 密钥配置（不入Git）
  api_keys.json.example
  proxy.json.example
  settings.json.example

knowledge/       ← 知识库
  弹窗处理标准流程.md
  1688爬取注意事项.md
  淘宝爬取注意事项.md
  评价数据抓取标准.md

data/            ← 结果输出（不入Git）
  taobao/  1688/  xiaohongshu/  douyin/
```

## 快速开始
```bash
# 1. 配置密钥
cp config/api_keys.json.example config/api_keys.json
cp config/proxy.json.example config/proxy.json
# 编辑填入真实密钥

# 2. 启动浏览器（Mac）
python platforms/mac/browser.py

# 3. 开始爬取
python -c "from core import *; s = BaseScraper(browser, '1688'); s.run()"
```

## 配置说明
- `api_keys.json`: AI密钥(SiliconFlow/DashScope)、Bark通知URL
- `proxy.json`: 代理配置(隧道/nas/直连) + Token
- `settings.json`: 爬取参数(时长/间隔/评价门槛)
