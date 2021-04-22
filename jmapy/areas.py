from dataclasses import dataclass
from typing import List


@dataclass
class Area:
    name: str
    code: str


@dataclass
class WeathersArea:
    area: Area
    weather_codes: List[str]
    weathers: List[str]
    winds: List[str]
    waves: List[str]


@dataclass
class TempsArea:
    area: Area
    temps: List[str]


@dataclass
class PopsArea:
    area: Area
    pops: List[str]
