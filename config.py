import token_op

BASE_URL = "https://muhanfrp.cn/api"


def get_headers():
    return {
        "Authorization": f"Bearer {token_op.read_token()}",
        "Accept": "application/json"
    }
