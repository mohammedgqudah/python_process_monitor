import sys
import redis
import time
from process_monitor import ConsumerMonitor


class MyConsumer:
    def __init__(self):
        redis_client = redis.Redis()
        self.monitor = ConsumerMonitor(redis_client=redis_client)
        self.monitor.run_signals_worker(sys.argv[1])

        while True:
            print("received event...")
            self.process_record({})
            time.sleep(3)

    def process_record(self, record):
        self.monitor.received_record()


MyConsumer()