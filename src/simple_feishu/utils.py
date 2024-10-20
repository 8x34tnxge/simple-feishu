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


def gen_general_content(tag: str, msg: str) -> Dict:
    return {
        "tag": tag,
        "text": msg,
    }


def gen_text_message(msg: str, secret: Optional[str] = None) -> Dict:
    ret = {
        "msg_type": "text",
        "content": gen_general_content("text", msg),
    }

    if secret is not None:
        ret = {**gen_signature(secret), **ret}

    return ret


def gen_signature(secret: str) -> Dict:
    timestamp = int(time.time())
    return {
        "timestamp": timestamp,
        "sign": gen_sign(timestamp, secret),
    }


def gen_nested_message(
    msg: str, msg_type: str = "text", secret: Optional[str] = None
) -> JsonStr:
    msg_body: Dict = {}
    if msg_type == "text":
        msg_body = gen_text_message(msg, secret)
    return json.dumps(msg_body)
