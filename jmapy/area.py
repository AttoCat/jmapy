from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import jmapy.city as city
import jmapy.region as region

from .request import _fetch_from_jma


@dataclass
class Area:
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


def fetch_areas(raw: bool = False) -> list[Area]:
    areas = _fetch_from_jma("/common/const/area.json")["class15s"]
    if raw:
        return areas
    return [Area(code, *value.values()) for code, value in areas.items()]


AREAS = fetch_areas()


def get_area(code: str) -> Optional[Area]:
    for area in AREAS:
        if code == area.code:
            return area
    else:
        return None


def search_area(name: str) -> Optional[Area]:
    for area in AREAS:
        if name in (area.name, area.en_name):
            return area
    else:
        return None
