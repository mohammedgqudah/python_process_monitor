import datetime as dt
import json


class Reader:
    def __init__(self, redis_client, prefix):
        self.redis_client = redis_client
        self._redis_hash_map_prefix = prefix

    def process_info(self, key):
        hash_map = self.redis_client.hgetall(key)

        return {
            **hash_map,
            'last_signal_age': (
                    dt.datetime.now() - dt.datetime.fromisoformat(hash_map.get('last_signal'))
            ).total_seconds(),
            'info': json.loads(hash_map['info'])
        }

    def read(self):
        keys = self.redis_client.keys("%s_*" % self._redis_hash_map_prefix)
        return {
            key.replace("%s_" % self._redis_hash_map_prefix, ""): self.process_info(key)
            for key in keys
        }
