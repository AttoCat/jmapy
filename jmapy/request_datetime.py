from datetime import datetime, timezone
from typing import Optional


class RequestDateTime:
    def __init__(self, request_datetime: Optional[datetime] = None) -> None:
        if request_datetime is None:
            self.request_datetime: str = self.datetime_to_string(
                datetime.utcnow())
            return
        if isinstance(request_datetime, datetime):
            self.request_datetime = self.datetime_to_string(
                request_datetime.astimezone(timezone.utc))
            return
        else:
            raise TypeError(
                f"RequestTime() argument must be datetime.datetime or str, not {type(request_datetime).__name__}")

    def __str__(self) -> str:
        return self.request_datetime

    @staticmethod
    def datetime_to_string(to_convert_datetime: datetime) -> str:
        return to_convert_datetime.strftime("%Y%m%d%H%M")


print(RequestDateTime(datetime.now()))
