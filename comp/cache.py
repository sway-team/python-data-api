import os
import time
import json
import hashlib
import env
from typing import Any, Optional

class FileCache:
    def __init__(self, cache_dir: str = env.RUNTIME_PATH + '/cache/', key_type: str = 'md5'):
        self.cache_dir = cache_dir
        self.key_type = key_type
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, key: str) -> str:
        # 用 key 的 md5 作为文件名，防止特殊字符
        if self.key_type == 'md5':
            key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
            file_name = f'{key_hash}.cache'
        else:
            file_name = key
            
        return os.path.join(self.cache_dir, file_name)
    
    def get_all_keys(self) -> list:
        return [f for f in os.listdir(self.cache_dir) if f.endswith('.cache')]

    def set(self, key: str, value: Any, expire: int = 3600):
        """
        保存缓存
        :param key: 缓存 key
        :param value: 缓存内容（可序列化为 json）
        :param expire: 失效时间（秒）
        expire = 0 表示永不过期
        """
        cache_path = self._get_cache_path(key)
        expire_at = int(time.time()) + expire if expire > 0 else 0
        data = {
            'expire_at': expire_at,
            'value': value
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存内容，若不存在或已过期返回 None
        """
        cache_path = self._get_cache_path(key)
        if not os.path.exists(cache_path):
            return None
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            expire_at = data.get('expire_at', 0)
            if expire_at > 0 and time.time() > expire_at:
                # 已过期，自动删除
                os.remove(cache_path)
                return None
            return data.get('value')
        except Exception:
            # 文件损坏等异常
            return None

    def delete(self, key: str):
        """
        删除缓存
        """
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            os.remove(cache_path)
