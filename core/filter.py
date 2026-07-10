"""刷单评价过滤器"""
import re
from collections import defaultdict

class FakeReviewFilter:
    """刷单检测"""

    FAKE_USER_PATTERN = re.compile(r'^t\*+\d+', re.I)  # t***123

    def is_fake(self, user, text):
        # 用户名: t + *** + 数字
        if user and self.FAKE_USER_PATTERN.search(user):
            return True
        # 内容太短
        if len(text) < 8:
            return True
        # 中文太少
        if len(re.findall(r'[\u4e00-\u9fa5]', text)) < 4:
            return True
        return False

    def find_duplicates(self, reviews, min_len=6, max_len=8, min_count=3):
        """检测重复短句"""
        phrases = defaultdict(list)
        for idx, r in enumerate(reviews):
            t = r.get('text', '') or r.get('content', '')
            for size in range(min_len, max_len + 1):
                for i in range(0, max(1, len(t) - size + 1)):
                    phrase = t[i:i+size]
                    if re.match(r'^[\u4e00-\u9fa5]{%d}$' % size, phrase):
                        if idx not in phrases[phrase]:
                            phrases[phrase].append(idx)
        return {p: ids for p, ids in phrases.items() if len(ids) >= min_count}

    def filter_all(self, reviews):
        """全量过滤"""
        dup = self.find_duplicates(reviews)
        dup_indices = set()
        for indices in dup.values():
            dup_indices.update(indices)

        real, fake = [], 0
        for i, r in enumerate(reviews):
            text = r.get('text', '') or r.get('content', '')
            user = r.get('user', '')
            if self.is_fake(user, text) or i in dup_indices:
                fake += 1
                continue
            real.append(r)
        return real, fake, dup
