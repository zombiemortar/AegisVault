import time

class SessionManager:
    def __init__(self, timeout=300):  # 300 seconds (5 minutes) default
        self.timeout = timeout
        self.last_activity = time.time()

    def reset_activity(self):
        self.last_activity = time.time()

    def check_timeout(self):
        return (time.time() - self.last_activity) > self.timeout