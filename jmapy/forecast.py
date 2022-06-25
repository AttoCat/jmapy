from __future__ import annotations

from dataclasses import InitVar, dataclass
from datetime import datetime
from typing import List, Optional, Tuple

from dacite import Config, from_dict
from humps import decamelize

from .parse_models import Area, ParsedPops, ParsedTemps, ParsedWeathers
from .request import _fetch_from_jma


def get_forecast(code: str, raw: bool = False):
    if not isinstance(raw, bool):
        raise TypeError(f"raw argument must be bool, not {type(raw).__name__}")
    forecast = _fetch_from_jma(f"/forecast/data/forecast/{code}.json")[0]
    if raw:
        return forecast
    return from_dict(Forecast, decamelize(forecast), Config({datetime: datetime.fromisoformat}, cast=[tuple]))


@dataclass
class Forecast:
    publishing_office: str
    report_datetime: datetime
    time_series: Tuple[WeatherForecasts, PopForecasts, TempForecasts]

    def __post_init__(self):
        self.weather_forecasts, self.pop_forecasts, self.temp_forecasts = self.time_series

    def _get_forecast_from_areas(self, area: str, forecasts):
        if not isinstance(area, str):
            raise TypeError(f"area argument must be str, not {type(area).__name__}")
        for forecast in forecasts.areas:
            if area not in (forecast.area.name, forecast.area.code):
                continue
            return forecast
        else:
            return None

    def get_weathers(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.weather_forecasts)
        if forecast is None:
            return None
        return Weathers(
            area=forecast.area, weathers=forecast.weathers, time_defines=self.weather_forecasts.time_defines
        )

    def get_weather_codes(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.weather_forecasts)
        if forecast is None:
            return None
        return WeatherCodes(
            area=forecast.area, weather_codes=forecast.weather_codes, time_defines=self.weather_forecasts.time_defines
        )

    def get_winds(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.weather_forecasts)
        if forecast is None:
            return None
        return Winds(area=forecast.area, winds=forecast.winds, time_defines=self.weather_forecasts.time_defines)

    def get_waves(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.weather_forecasts)
        if forecast is None:
            return None
        return Winds(area=forecast.area, winds=forecast.waves, time_defines=self.weather_forecasts.time_defines)

    def get_pops(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.pop_forecasts)
        if forecast is None:
            return None
        return Pops(area=forecast.area, pops=forecast.pops, time_defines=self.pop_forecasts.time_defines)

    def get_temps(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.temp_forecasts)
        if forecast is None:
            return None
        return Temps(area=forecast.area, temps=forecast.temps, time_defines=self.temp_forecasts.time_defines)


@dataclass
class OnedayForecast:
    date: datetime
    publishing_office: str
    weather: str
    weather_code: str
    wave: Optional[str]
    wind: str
    pops: InitVar[List[str]]
    pop_time_defines: InitVar[List[datetime]]

    def __post_init__(self, pops: List[str], pop_time_defines: List[datetime]):
        p00to06 = p06to12 = p12to18 = p18to24 = None
        for pop_time_define, pop in zip(pop_time_defines, pops):
            if pop_time_define.day != self.date:
                continue
            if pop_time_define.hour == 0:
                p00to06 = pop
            elif pop_time_define.hour == 6:
                p06to12 = pop
            elif pop_time_define.hour == 12:
                p12to18 = pop
            elif pop_time_define.hour == 18:
                p18to24 = pop
            self.pops = [p00to06, p06to12, p12to18, p18to24]


@dataclass
class _BaseForecast:
    area: Area
    time_defines: List[datetime]


@dataclass
class Weathers(_BaseForecast):
    weathers: List[str]


@dataclass
class WeatherCodes(_BaseForecast):
    weather_codes: List[str]


@dataclass
class Winds(_BaseForecast):
    winds: List[str]


@dataclass
class Waves(_BaseForecast):
    waves: Optional[List[str]]


@dataclass
class Pops(_BaseForecast):
    pops: List[str]


@dataclass
class Temps(_BaseForecast):
    temps: List[str]


@dataclass
class WeatherForecasts:
    time_defines: List[datetime]
    areas: List[ParsedWeathers]


@dataclass
class PopForecasts:
    time_defines: List[datetime]
    areas: List[ParsedPops]


@dataclass
class TempForecasts:
    time_defines: List[datetime]
    areas: List[ParsedTemps]
