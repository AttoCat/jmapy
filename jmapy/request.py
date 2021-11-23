from json import loads

from requests import get

BASE = "https://www.jma.go.jp/bosai"


def _jma_get(url: str, **kwargs):
    response = get(f"{BASE}{url}", **kwargs)
    response.raise_for_status()
    return loads(response.text.replace("\u3000", " "))
