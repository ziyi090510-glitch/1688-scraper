# InstHunter — Instagram网红内容采集平台

## 定位
Instagram内容采集与展示，服务宠物定制业务

## 核心能力
- 双引擎：Apify云端采集 + instagrapi本地采集
- 千问视觉模型图片识别（qwen3-vl-plus）
- AI过滤流水线（图片分类 + 文本翻译）
- IHDS数据服务 + photostack照片管理
- Web UI控制台（5页面）

## 关键架构决策
- pydantic-settings .env 用 __file__ 计算绝对路径（防止nohup CWD问题）
- `********`占位符不覆盖真实API Key
- 时区统一北京时间（6文件14处修改）
- 多源降级：源1→源2→源3依次尝试

## 部署
152服务器，端口29528，独立venv
