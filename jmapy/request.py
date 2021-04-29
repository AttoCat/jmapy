from json import loads

from humps import decamelize
from requests import get

from .errors import InternalServerError, NotFound

BASE = "https://www.jma.go.jp/bosai"


def _jma_get(url: str, **kwargs):
    response = get(f"{BASE}{url}", **kwargs)
    if response.status_code == 404:
        raise NotFound
    elif response.status_code == 500:
        raise InternalServerError
    encoded_text = decamelize(response.text.replace("\u3000", " "))
    return loads(encoded_text)
