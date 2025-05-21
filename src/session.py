import threading
import time

SESSION_TIMEOUT = 300  # 30-second timeout
session_expire_event = threading.Event()

class SessionManager:
    def __init__(self):
        self.active = False
        self.username = None
        self.start_time = None

    def start_session(self, username):
        """Starts a session and monitors expiration."""
        self.active = True
        self.username = username
        self.start_time = time.time()
        threading.Thread(target=self.monitor_session, daemon=True).start()  # ✅ Run in background

    def validate_session(self):
        """Checks if the session is still active."""
        if not self.active or (time.time() - self.start_time) >= SESSION_TIMEOUT:
            self.expire_session()
            return False
        return True

    def refresh_session(self):
        """Refreshes session timer when activity occurs."""
        self.start_time = time.time()
        #print("🔄 Session timer refreshed.")

    def expire_session(self):
        """Handles session expiration without duplicate execution."""
        if not self.active:  # ✅ Prevent multiple calls
            return

        print("\n❌ Session expired due to inactivity.")
        self.active = False
        self.username = None
        session_expire_event.set()  # ✅ Signal expiration only once
        print(f"DEBUG: session_expire_event.is_set() → {session_expire_event.is_set()}")  # 🛠 Confirms event signal

    def monitor_session(self):
        """Monitors session timeout and expires if idle for too long."""
        while self.active:
            time.sleep(5)  # ✅ Check every 5 seconds

            if not self.validate_session():
                break