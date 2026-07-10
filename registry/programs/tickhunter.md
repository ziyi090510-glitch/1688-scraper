# TickHunter — TikTok内容采集器

## 定位
基于InstHunter架构复制的TikTok平台采集器

## 核心能力
- 架构克隆模式（cp -r复制，不修改原项目）
- Apify TikTok Scraper集成
- 千问视觉封面分析（qwen3-vl-plus）
- 三源降级下载（Apify KVS→VPS代理→直连）
- 循环计划调度器（scrape_plans.json）
- 连续5轮0条自动暂停

## 关键架构
- 端口29540，独立数据库tickhunter.db
- 独立venv，避免依赖冲突
- 深色主题Web UI（5页面）
