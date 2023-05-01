from file.project_paths import *
from datetime import datetime

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        self.clear()

        with open(self.log_path, "w") as f:
            f.write(f"Last run at {datetime.now()}\n")

    def log(self, data):
        with open(self.log_path, "a") as f:
            f.write(f"{datetime.now()}: {data}\n")

    def clear(self):
        try:
            open(self.log_path, "w").close()
        except FileNotFoundError:
            pass