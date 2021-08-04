# Process Monitor
A python tool that utilizes redis to keep track of long-running processes.
It triggers a signal every n seconds, so that a health check/monitoring API can view
the last signal timestamp.

# Requirements
- redis

# Configuration 
- redis connection parameters to be passed directly to the redis client.

# Usage
## Consumer
```python
from process_monitor import Monitor


class MyProcess:
    def __init__(self):
        self.monitor = Monitor(args)
        self.monitor.run_signals_worker('process-name')
```

## API - Monitor
```python
@route('/check-process')
def check_process():
    monitor = Monitor(args)
    results = monitor.read()
    # [{
    #     'name': 'process-name',
    #     'last_signal': '2021-08-03 22:36:55.457416',
    #     'last_signal_age': 3,
    #     'info': {
    #       'x': 1
    #     }
    # }]
    return Response(data=results)
```

# Example
![example](https://github.com/mohammedgqudah/python_process_monitor/blob/master/process_monitor_read_example.gif?raw=true)
# Custom Monitors

## Kinesis Consumer Monitor
```python
from process_monitor import ConsumerMonitor

class MyConsumer:
    def __init__(self):
        self.monitor = ConsumerMonitor(args)
        self.monitor.run_signals_worker('consumer-name')

    def process_record(self, record):
        self.monitor.received_record()
        ...
```