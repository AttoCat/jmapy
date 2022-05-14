from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import jmapy.area as area

from .request import _fetch_from_jma


@dataclass
class City:
    code: str
    name: str
    en_name: str
    kana: str
    _parent: str

    @property
    def area(self) -> area.Area:
        return area.get_area(self._parent)


def fetch_cities(raw: bool = False) -> list[City]:
    cities = _fetch_from_jma("/common/const/area.json")["class20s"]
    if raw:
        return cities
    return [City(code, *value.values()) for code, value in cities.items()]


CITIES = fetch_cities()


def get_city(code: str) -> Optional[City]:
    for city in CITIES:
        if code == city.code:
            return city
    else:
        return None


def search_city(name: str) -> Optional[City]:
    for city in CITIES:
        if name in (city.name, city.en_name, city.kana):
            return city
    else:
        return None
