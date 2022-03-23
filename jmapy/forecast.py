from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

from dacite import Config, from_dict
from humps import decamelize

from .parse_models import Area, ParsedPops, ParsedTemps, ParsedWeathers
from .request import _jma_get


def get_forecast(area_code: str, raw: bool = False):
    if not isinstance(raw, bool):
        raise TypeError(f"raw argument must be bool, not {type(raw).__name__}")
    forecast = _jma_get(
        f"/forecast/data/forecast/{area_code}.json")[0]
    if raw:
        return forecast
    return from_dict(Forecast, decamelize(forecast), Config(
        {datetime: datetime.fromisoformat}, cast=[tuple]))


@dataclass
class Forecast:
    publishing_office: str
    report_datetime: datetime
    time_series: Tuple[WeatherForecasts, PopForecasts, TempForecasts]

    def __post_init__(self):
        self.weather_forecasts, self.pop_forecasts, self.temp_forecasts = self.time_series

    @property
    def available_areas(self):
        weather_areas = [
            forecast.area for forecast in self.weather_forecasts.areas]
        pop_areas = [forecast.area for forecast in self.pop_forecasts.areas]
        temp_areas = [forecast.area for forecast in self.temp_forecasts.areas]
        available_areas = {
            "weather": weather_areas,
            "weather_code": weather_areas,
            "wind": weather_areas,
            "wind": weather_areas,
            "wave": weather_areas,
            "pop": pop_areas,
            "temp": temp_areas
        }
        return available_areas

    def _get_forecast_from_areas(self, area: str, forecasts):
        if not isinstance(area, str):
            raise TypeError(
                f"area argument must be str, not {type(area).__name__}")
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
            area=forecast.area, weathers=forecast.weathers, time_defines=self.weather_time_defines)

    def get_weather_codes(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.weather_forecasts)
        if forecast is None:
            return None
        return WeatherCodes(
            area=forecast.area, weather_codes=forecast.weather_codes, time_defines=self.weather_time_defines)

    def get_winds(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.weather_forecasts)
        if forecast is None:
            return None
        return Winds(area=forecast.area, winds=forecast.winds,
                     time_defines=self.weather_time_defines)

    def get_waves(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.weather_forecasts)
        if forecast is None:
            return None
        return Winds(area=forecast.area, winds=forecast.winds,
                     time_defines=self.weather_time_defines)

    def get_pops(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.pop_forecasts)
        if forecast is None:
            return None
        return Pops(area=forecast.area, winds=forecast.winds,
                    time_defines=self.pop_forecasts.time_defines)

    def get_temps(self, area: str):
        forecast = self._get_forecast_from_areas(area, self.temp_forecasts)
        if forecast is None:
            return None
        return Temps(area=forecast.area, temps=forecast.temps,
                     time_defines=self.temp_forecasts.time_defines)


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
    waves: List[str]


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
