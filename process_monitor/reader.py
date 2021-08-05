import datetime as dt
import asyncio
import functools
import json

import aioredis


class Reader:
    _redis_hash_map_prefix = "process_monitor"

    def __init__(self, redis_client):
        assert redis_client.connection_pool.connection_kwargs.get('decode_responses'), \
            "Redis instance must have decode_responses=True"
        self.redis_client = redis_client
        self._async = isinstance(redis_client, aioredis.Redis)
        self.asyncio_event_loop = None

    @property
    @functools.lru_cache()
    def get_event_loop(self):
        return asyncio.get_event_loop()

    def async_call(self, function):
        this = self

        def wrap(*args, **kwargs):
            if this._async:
                return this.get_event_loop.run_until_complete(function(*args, **kwargs))
            return function(*args, **kwargs)

        return wrap

    def process_info(self, key):
        hash_map = self.async_call(self.redis_client.hgetall)(key)

        return {
            **hash_map,
            'last_signal_age': (
                    dt.datetime.now() - dt.datetime.fromisoformat(hash_map.get('last_signal'))
            ).total_seconds(),
            'info': json.loads(hash_map['info'])
        }

    async def async_process_info(self, key):
        hash_map = await self.redis_client.hgetall(key)

        return {
            **hash_map,
            'last_signal_age': (
                    dt.datetime.now() - dt.datetime.fromisoformat(hash_map.get('last_signal'))
            ).total_seconds(),
            'info': json.loads(hash_map['info'])
        }

    def read(self):
        keys = self.async_call(self.redis_client.keys)("%s_*" % self._redis_hash_map_prefix)
        return {
            key.replace("%s_" % self._redis_hash_map_prefix, ""): self.process_info(key)
            for key in keys
        }

    async def async_read(self):
        keys = await self.redis_client.keys("%s_*" % self._redis_hash_map_prefix)
        return {
            key.replace("%s_" % self._redis_hash_map_prefix, ""): await self.async_process_info(key)
            for key in keys
        }
