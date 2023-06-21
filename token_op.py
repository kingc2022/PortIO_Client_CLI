import base64
import os.path

import requests

import config
import funcs as func


def verify_token(token: str):
    func.warning("正在检测 Token 是否有效")
    response = requests.get(f"{config.BASE_URL}/user", headers={
        "Authorization": f"Bearer {token}"
    })
    response.encoding = response.apparent_encoding
    # 检测返回值是否为 HTML (若是, 则 Token 无效)
    if "navbar-brand" in response.text and "LoliArt Account" in response.text:
        func.error("Token 无效")
        return False
    else:
        func.success("Token 有效")
        return True


def write_token(token: str):
    if verify_token(token):
        with open("token.txt", 'w', encoding='UTF-8') as f:
            f.write(base64.urlsafe_b64encode(token.encode()).decode())
        func.success("写入成功")
        func.pause_and_exit()
    else:
        func.pause_and_exit()


def read_token():
    if os.path.exists("token.txt") and os.path.isfile("token.txt"):
        with open("token.txt", 'r', encoding='UTF-8') as f:
            token = f.read()
        return base64.urlsafe_b64decode(token).decode()
    else:
        return None
