from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import jmapy.county as county

from .request import _fetch_from_jma


@dataclass
class Part:
    code: int
    name: str
    en_name: str
    office_name: str
    _children: list[str]

    @property
    def counties(self) -> list[county.County]:
        return [county.get_county(child) for child in self._children]


def fetch_parts(raw: bool = False) -> list[Part]:
    parts = _fetch_from_jma("/common/const/area.json")["centers"]
    if raw:
        return parts
    return [Part(code, *value.values()) for code, value in parts.items()]


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
