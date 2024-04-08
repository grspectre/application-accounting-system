import requests
from .util import Config
from typing import Optional


def get_access_token(code: str) -> Optional[dict]:
    query = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': Config.env_get('YANDEX_CLIENT_ID'),
        'client_secret': Config.env_get('YANDEX_CLIENT_SECRET'),
    }
    r = requests.post('https://oauth.yandex.ru/token', data=query)
    print(r.status_code)
    if r.status_code == 200:
        return r.json()
    return None
