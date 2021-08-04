import json
import redis
import time
from process_monitor import ConsumerMonitor


class Read:
    def __init__(self):
        redis_client = redis.Redis(decode_responses=True)
        monitor = ConsumerMonitor(redis_client=redis_client)
        while True:
            print(json.dumps(monitor.read(), indent=4))
            time.sleep(5)


Read()
