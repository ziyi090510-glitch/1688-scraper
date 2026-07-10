# RedHunter 踩过的坑

1. **关键词回收死循环**：回收→激活→抓取→又标记失效
   - 修复：删除激进跳过逻辑，仅依赖consecutive_zero计数器

2. **搜索退化**：73%搜索是退化词「宠物写真×3」
   - 修复：删除退化逻辑，search_history去重

3. **浏览器守护断开**：x11vnc未启动导致无法远程查看
   - 修复：全组件守护+cron每分钟5项健康监控

4. **Python raw string中JS正则转义**：\\d写成了\\\d
   - 修复：写成文件或String.fromCharCode规避

5. **风控应对**：淘宝反检测机制
   - 修复：Windows Server+RDP天然不被检测；独立浏览器+临时号
