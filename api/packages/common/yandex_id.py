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
    if r.status_code == 200:
        return r.json()
    return None


def get_user_info(access_token: str) -> Optional[dict]:
    headers = {
        'Authorization': 'Oauth {}'.format(access_token)
    }
    r = requests.get('https://login.yandex.ru/info?format=json', headers=headers)
    if r.status_code == 200:
        return r.json()
    return None
