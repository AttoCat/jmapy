from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Union

from dacite import Config, from_dict
from humps import decamelize

from .parse_models import (WeeklyPops, WeeklyPrecipAverage, WeeklyTempAverage,
                           WeeklyTemps)
from .request import _fetch_from_jma


def get_weekly_forecast(area_code: int | str, raw: bool = False):
    if not isinstance(raw, bool):
        raise TypeError(f"raw argument must be bool, not {type(raw).__name__}")
    weekly_forecast = _fetch_from_jma(
        f"/forecast/data/forecast/{area_code}.json")[1]
    if raw:
        return weekly_forecast
    return from_dict(WeeklyForecast, decamelize(weekly_forecast),
                     Config({datetime: datetime.fromisoformat}))


@dataclass
class WeeklyForecast:
    publishing_office: str
    report_datetime: datetime
    time_series: List[TimeSeries]
    temp_average: WeeklyTempAverage
    precip_average: WeeklyPrecipAverage


@dataclass
class TimeSeries:
    time_defines: List[datetime]
    areas: List[Union[WeeklyPops, WeeklyTemps]]
