import json
import time
from process_monitor import Reader
import redis


class Read:
    def __init__(self):
        redis_client = redis.Redis(decode_responses=True)
        monitor_reader = Reader(redis_client=redis_client)
        while True:
            print(json.dumps(monitor_reader.read(), indent=4))
            time.sleep(5)


Read()
