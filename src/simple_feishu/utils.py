import base64
import time
import json
import hashlib
import hmac
from typing import Dict, Optional

type JsonStr = str


def gen_sign(timestamp: int, secret: str) -> str:
    # 拼接timestamp和secret
    string_to_sign = "{}\n{}".format(timestamp, secret)
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


def gen_normal_message(msg: str, msg_type: str) -> Dict:
    return {
        "msg_type": msg_type,
        "content": {
            "text": msg,
        },
    }


def gen_signed_message(msg: str, msg_type: str, secret: str) -> Dict:
    timestamp = int(time.time())
    return {
        **{
            "timestamp": timestamp,
            "sign": gen_sign(timestamp, secret),
        },
        **gen_normal_message(msg, msg_type),
    }


def gen_nested_message(
    msg: str, msg_type: str = "text", secret: Optional[str] = None
) -> JsonStr:
    msg_body: Dict = (
        gen_normal_message(msg, msg_type)
        if secret is None
        else gen_signed_message(msg, msg_type, secret)
    )
    return json.dumps(msg_body)
