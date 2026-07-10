# 1688-Scraper — 多平台电商爬虫共享库

Mac / Windows 通用，Cherry Claw 标准爬虫程序库。

## 目录结构

```
core/              ← 跨平台通用（Mac/Win 共享，不可平台差异化）
  scraper.py          核心引擎（CDP连接、页面导航、结果持久化）
  reviews.py          评价提取（淘宝滚轮 + 1688 Drawer分页）
  filter.py           刷单过滤器（t***数字 + 重复短句 + 字数校验）
  ai_vision.py        图片识别（SiliconFlow Qwen3-VL-8B）
  popup.py            弹窗检测（5维：文本+DOM+URL+标题+遮罩）
  config.py           全局配置（API密钥、代理、CDP端口、平台探针）

platforms/          ← 分平台（Mac/Win各自维护）
  mac/browser.py      Chrome启动（Mac应用路径）
  windows/browser.py  Chrome启动（Win exe路径）

database/           ← 结果持久化
  storage.py          按平台分目录 + 二级分类自动创建

config/             ← 密钥和配置模板（不入Git）
  api_keys.json.example   AI密钥（SiliconFlow/DashScope）+ Bark
  proxy.json.example      代理配置（隧道/NAS/直连 + Token）
  settings.json.example   爬取参数（时长/间隔/评价门槛）

knowledge/          ← 知识库（每次爬虫任务前必读）
  1688爬取注意事项.md
  淘宝爬取注意事项.md
  弹窗处理标准流程.md
  评价数据抓取标准.md

data/               ← 结果输出（不入Git，按平台分目录）
  taobao/  1688/  xiaohongshu/  douyin/
```

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/ziyi090510-glitch/1688-scraper.git

# 2. 配置密钥
cp config/api_keys.json.example config/api_keys.json
cp config/proxy.json.example config/proxy.json
# 编辑填入真实密钥

# 3. 安装依赖
pip install playwright Pillow httpx paramiko
playwright install chromium

# 4. 启动浏览器（Mac）
python platforms/mac/browser.py
# （登录1688/淘宝后继续）

# 5. 运行爬虫
python -c "from core.scraper import BaseScraper; ..."
```

## 关键标准（所有爬虫程序必须遵守）

### 弹窗检测（最高优先级）
- 每次 `goto()` 前后 + 评论滚动前后 + 每个商品处理前
- 5维检测：文本关键词 + DOM结构 + URL重定向 + 标题变化 + baxia遮罩
- 弹窗出现 → 立即停止 → Bark通知 → 手动处理 → 绝不自动关闭

### 评价提取标准
- 淘宝：`pg.locator('[class*="footer"]').filter(has_text='查看全部评价').click()` → `pg.mouse.wheel(0,800)` 逐段滚动
- 1688：`.evaluation-more .ant-btn` 打开Drawer → `ant-pagination-item` 翻页
- 限取200条

### 刷单过滤
- 用户名 `t***数字` → 刷单
- 内容 <8字 或 中文 <4字 → 无效
- 同商品 ≥3次相同6-8字短句 → 刷单

### 服务器连接速查
| 服务器 | IP | 用户 | 认证 |
|--------|-----|------|------|
| 30服务器(Win) | 122.51.32.30 | Administrator | coze.pem |
| 152服务器(Ubuntu) | 124.223.64.152 | ubuntu | coze.pem |
| NAS(群晖) | 192.168.0.21 | yang | 密码 |

### GitHub操作
- Token用 `ghp_` 开头的Classic PAT（Fine-grained PAT不能git push）
- Token权限：repo（全部仓库读写）
