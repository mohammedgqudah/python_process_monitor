import datetime as dt
import json


class Reader:
    _redis_hash_map_prefix = "process_monitor"

    def __init__(self, redis_client):
        assert redis_client.connection_pool.connection_kwargs.get('decode_responses'), \
            "Redis instance must have decode_responses=True"
        self.redis_client = redis_client

    @classmethod
    def _process_info(cls, hash_map):
        return {
            **hash_map,
            'last_signal_age': (
                    dt.datetime.now() - dt.datetime.fromisoformat(hash_map.get('last_signal'))
            ).total_seconds(),
            'info': json.loads(hash_map['info'])
        }

    def process_info(self, key):
        return self._process_info(self.redis_client.hgetall(key))

    async def async_process_info(self, key):
        return self._process_info(await self.redis_client.hgetall(key))

    def _get_keys(self):
        return self.redis_client.keys("%s_*" % self._redis_hash_map_prefix)

    def read(self):
        keys = self._get_keys()
        return {
            key.replace("%s_" % self._redis_hash_map_prefix, ""): self.process_info(key)
            for key in keys
        }

    async def async_read(self):
        keys = await self._get_keys()
        return {
            key.replace("%s_" % self._redis_hash_map_prefix, ""): await self.async_process_info(key)
            for key in keys
        }
