from json import loads

from humps import decamelize
from requests import get

from .errors import InternalServerError, NotFound

BASE = "https://www.jma.go.jp/bosai"


def _jma_get(url: str, raw: bool = False, **kwargs):
    response = get(f"{BASE}{url}", **kwargs)
    if response.status_code == 404:
        raise NotFound
    elif response.status_code == 500:
        raise InternalServerError
    if raw:
        return response.json()
    encoded_text = response.text.replace("\u3000", " ")
    return decamelize(loads(encoded_text))
