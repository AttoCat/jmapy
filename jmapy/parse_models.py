from dataclasses import dataclass
from typing import List


@dataclass
class Area:
    name: str
    code: str


@dataclass
class ParsedWeathers:
    area: Area
    weather_codes: List[str]
    weathers: List[str]
    winds: List[str]
    waves: List[str]


@dataclass
class ParsedTemps:
    area: Area
    temps: List[str]


@dataclass
class ParsedPops:
    area: Area
    pops: List[str]


@dataclass
class WeeklyPops:
    area: Area
    weather_codes: List[str]
    pops: List[str]
    reliabilities: List[str]


@dataclass
class WeeklyTemps:
    area: Area
    temps_min: List[str]
    temps_min_upper: List[str]
    temps_min_lower: List[str]
    temps_max: List[str]
    temps_max_upper: List[str]
    temps_max_lower: List[str]


@dataclass
class TempAverage:
    area: Area
    min: str
    max: str


@dataclass
class WeeklyTempAverage:
    areas: List[TempAverage]


@dataclass
class PrecipAverage:
    area: Area
    min: str
    max: str


@dataclass
class WeeklyPrecipAverage:
    areas: List[PrecipAverage]
