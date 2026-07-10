# AI图片识别

## API
SiliconFlow Qwen3-VL-8B-Instruct

## 流程
1. PIL压缩到512px（减少token消耗80%+）
2. Base64编码
3. 调SiliconFlow vision API
4. 返回分类结果

## 配置
api_keys.json → siliconflow.api_key
