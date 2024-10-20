import subprocess
from typing import Optional


class FeishuRobot:
    def __init__(self, token: str, secret: Optional[str] = None) -> None:
        self.token = token
        self.secret = secret

    def send_message(self, message: str) -> int:
        notify_command = [
            "curl",
            *["-X", "POST"],
            *["-H", "Content-Type: application/json"],
            *["-d", message],
            self.token,
        ]
        return subprocess.run(notify_command).returncode
