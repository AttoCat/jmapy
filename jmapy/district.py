from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import jmapy.city as city
import jmapy.region as region

from .request import _fetch_from_jma


@dataclass
class District:
    code: str
    name: str
    en_name: str
    _parent: str
    _children: list[str]

    @property
    def region(self) -> region.Region:
        return region.get_region(self._parent)

    @property
    def cities(self) -> list[city.City]:
        return [city.get_city(child) for child in self._children]


def fetch_districts(raw: bool = False) -> list[District]:
    districts = _fetch_from_jma("/common/const/area.json")["class15s"]
    if raw:
        return districts
    return [District(code, *value.values()) for code, value in districts.items()]


DISTRICTS = fetch_districts()


def get_district(code: str) -> Optional[District]:
    for district in DISTRICTS:
        if code == district.code:
            return district
    else:
        return None


def search_district(name: str) -> Optional[District]:
    for district in DISTRICTS:
        if name in (district.name, district.en_name):
            return district
    else:
        return None
