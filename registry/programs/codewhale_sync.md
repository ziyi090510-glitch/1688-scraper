# CodeWhale 对话实时同步系统

## 定位
AI对话记录实时同步到Web展示页面

## 核心能力
- Bash脚本+HTTP API+JSON文件存储
- 去重策略：最后消息content+timestamp比较
- L0优先级规则强制每次对话执行同步
- 6位房间代码唯一标识
- 零外部依赖（纯Python标准库）

## 关键发现
- CodeWhale 0.8.47无UI语言配置→通过instructions.md规则实现中文
- 同步存在时间窗口缺失→L0强制规则保障
