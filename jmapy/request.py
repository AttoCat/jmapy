from json import loads

from requests import get

from .errors import InternalServerError, NotFound

BASE = "https://www.jma.go.jp/bosai"


def _jma_get(url: str, **kwargs):
    response = get(f"{BASE}{url}", **kwargs)
    if response.status_code == 404:
        raise NotFound
    elif response.status_code == 500:
        raise InternalServerError
    return loads(response.text)
