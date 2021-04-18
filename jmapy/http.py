from requests import get

from errors import InternalServerError, NotFound


def _jma_get(url: str, **kwargs):
    response = get(url, kwargs)
    if response.status_code == 404:
        raise NotFound
    elif response.status_code == 500:
        raise InternalServerError
    return response.json()
