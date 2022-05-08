from dataclasses import dataclass
from typing import Optional

from humps import decamelize

from .request import _fetch_from_jma


@dataclass
class Part:
    code: int
    name: str
    en_name: str
    office_name: str
    children: list[str]


def fetch_parts(raw: bool = False):
    parts = _fetch_from_jma("/common/const/area.json")["centers"]
    if raw:
        return parts
    return [Part(k, *v.values()) for k, v in decamelize(parts).items()]


PARTS = fetch_parts()


def get_part(code: str) -> Optional[Part]:
    for part in PARTS:
        if code == part.code:
            return part
    else:
        return None


def search_part(name: str) -> Optional[Part]:
    for part in PARTS:
        if name in (part.name, part.en_name):
            return part
    else:
        return None
