from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import jmapy.part as part
import jmapy.region as region

from .request import _fetch_from_jma


@dataclass
class County:
    code: str
    name: str
    en_name: str
    office_name: str
    _parent: str
    _children: list[str]

    @property
    def part(self) -> part.Part:
        return part.get_part(self._parent)

    @property
    def regions(self) -> list[region.Region]:
        return [region.get_region(child) for child in self._children]


def fetch_counties(raw: bool = False) -> list[County]:
    counties = _fetch_from_jma("/common/const/area.json")["offices"]
    if raw:
        return counties
    return [County(code, *value.values()) for code, value in counties.items()]


COUNTIES = fetch_counties()


def get_county(code: str) -> Optional[County]:
    for county in COUNTIES:
        if code == county.code:
            return county
    else:
        return None


def search_county(name: str) -> Optional[County]:
    for county in COUNTIES:
        if name in (county.name, county.en_name):
            return county
    else:
        return None
