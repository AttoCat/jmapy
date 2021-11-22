from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

from dacite import Config, from_dict
from humps import decamelize

from .parse_models import Area, ParsedPops, ParsedTemps, ParsedWeathers
from .request import _jma_get


def get_forecast(area_code: str, raw: bool = False):
    if type(raw) is not bool:
        raise TypeError(f"raw argument must be bool, not {type(raw).__name__}")
    forecast = _jma_get(
        f"/forecast/data/forecast/{area_code}.json")[0]
    if raw:
        return forecast
    return from_dict(Forecast, decamelize(forecast), Config({datetime: datetime.fromisoformat}, cast=[tuple]))


@dataclass
class Forecast:
    publishing_office: str
    report_datetime: datetime
    time_series: Tuple[WeathersTimeSeries, PopsTimeSeries, TempsTimeSeries]

    def get_weathers(self, area: str):
        if not isinstance(area, str):
            raise TypeError(
                f"area argument must be bool, not {type(area).__name__}")
        for item in self.time_series[0].areas:
            if area not in (item.area.name, item.area.code):
                continue
            return Weathers(item.area, item.weathers, self.time_series[0].time_defines)
        else:
            return None


@dataclass
class Weathers:
    area: Area
    weathers: List[str]
    time_defines: List[datetime]


@dataclass
class WeathersTimeSeries:
    time_defines: List[datetime]
    areas: List[ParsedWeathers]


@dataclass
class PopsTimeSeries:
    time_defines: List[datetime]
    areas: List[ParsedPops]


@dataclass
class TempsTimeSeries:
    time_defines: List[datetime]
    areas: List[ParsedTemps]
