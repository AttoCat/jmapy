from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import jmapy.county as county

from .request import _fetch_from_jma


@dataclass
class Region:
    code: str
    name: str
    en_name: str
    _parent: str
    _children: list[str]

    @property
    def county(self) -> county.County:
        return county.get_county(self._parent)


def fetch_regions(raw: bool = False) -> list[Region]:
    regions = _fetch_from_jma("/common/const/area.json")["class10s"]
    if raw:
        return regions
    return [Region(code, *value.values()) for code, value in regions.items()]


REGIONS = fetch_regions()


def get_region(code: str) -> Optional[Region]:
    for region in REGIONS:
        if code == region.code:
            return region
    else:
        return None


def search_region(name: str) -> Optional[Region]:
    for region in REGIONS:
        if name in (region.name, region.en_name):
            return region
    else:
        return None
