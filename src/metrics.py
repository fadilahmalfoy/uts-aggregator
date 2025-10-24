from datetime import datetime

class Metrics:
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.received = 0
        self.unique_processed = 0
        self.duplicate_dropped = 0
        self.topics = set()

    def uptime(self):
        delta = datetime.utcnow() - self.start_time
        return f"{int(delta.total_seconds())}s"

metrics = Metrics()
