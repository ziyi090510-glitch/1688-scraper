"""AI 视觉识别 — SiliconFlow"""
import base64, io, logging
from .config import cfg as Cfg

log = logging.getLogger('ai_vision')

class AIVision:
    """图片识别 — 可压缩后调 SiliconFlow"""

    def __init__(self):
        cfg = Cfg.get()
        self.enabled = cfg.settings.get('image_recognition', {}).get('enabled', False)
        self.api_key = cfg.api_keys.get('siliconflow', {}).get('api_key', '')
        self.base_url = cfg.api_keys.get('siliconflow', {}).get('base_url', 'https://api.siliconflow.cn/v1')
        self.model = cfg.settings.get('image_recognition', {}).get('model', {}).get('name', 'Qwen/Qwen3-VL-8B-Instruct')

    @staticmethod
    def compress(filepath, max_dim=512, quality=75):
        """压缩图片到 max_dim px，返回 JPEG bytes"""
        try:
            from PIL import Image
            img = Image.open(filepath)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            w, h = img.size
            if max(w, h) > max_dim:
                img.thumbnail((max_dim, max_dim), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=quality, optimize=True)
            return buf.getvalue()
        except Exception as e:
            log.warning(f'图片压缩失败: {e}')
            return None

    async def analyze(self, image_b64, prompt, max_tokens=100):
        """异步调用视觉API"""
        if not self.enabled or not self.api_key:
            return None
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    f'{self.base_url}/chat/completions',
                    headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                    json={'model': self.model,
                          'messages': [{'role': 'user', 'content': [
                              {'type': 'text', 'text': prompt},
                              {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{image_b64}'}}
                          ]}], 'max_tokens': max_tokens, 'temperature': 0.1})
                if r.status_code == 200:
                    return r.json()['choices'][0]['message']['content'].strip()
                log.error(f'AI识别失败: {r.status_code}')
        except Exception as e:
            log.warning(f'AI识别异常: {e}')
        return None
