import subprocess
from typing import Optional
from .utils import gen_nested_message


class FeishuBot:
    def __init__(self, token: str, secret: Optional[str] = None) -> None:
        self.token = token
        self.secret = secret

    def send_message(self, message: str) -> int:
        notify_command = [
            "curl",
            *["-X", "POST"],
            *["-H", "Content-Type: application/json"],
            *["-d", gen_nested_message(message, "text", self.secret)],
            self.token,
        ]
        return subprocess.run(notify_command).returncode
