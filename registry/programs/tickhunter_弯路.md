# TickHunter 踩过的坑

1. **架构克隆时的依赖冲突**：直接复用insthunter venv导致包版本冲突
   - 修复：cp -r + 全局替换(项目名/端口/数据库) + 独立venv

2. **TikTok API数据格式不兼容**：Instagram模型字段不适用
   - 修复：SQLite模型适配TikTok特有字段

3. **封面图下载失败**：Apify CDN有时不可达
   - 修复：三源降级策略（KVS→VPS→直连）

4. **连续抓取0条不停止**：风控导致无结果但程序继续跑
   - 修复：连续5轮0条自动暂停+告警
