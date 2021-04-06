from datetime import datetime, timezone


class RequestDateTime:
    def __init__(self, request_datetime=datetime.utcnow()):
        if isinstance(request_datetime, int):
            request_datetime = str(request_datetime)
        if isinstance(request_datetime, datetime):
            if (request_datetime.tzinfo is None) or (request_datetime.tzinfo == "UTC"):
                self.request_datetime = self.datetime_to_string(
                    request_datetime)
                return
            if request_datetime.tzinfo and (request_datetime.tzinfo != "UTC"):
                self.request_datetime = self.datetime_to_string(
                    request_datetime.astimezone(timezone.utc))
                return
        elif isinstance(request_datetime, str):
            if self.is_convertible(request_datetime):
                self.request_datetime = request_datetime
            else:
                raise ValueError(
                    f"RequestTime() argument does not match the pattern. [specify a six-digit date. Ex:{RequestDateTime()}]")
        else:
            raise TypeError(
                f"RequestTime() argument must be datetime.datetime or str, not {type(request_datetime).__name__}")

    def __str__(self):
        return self.request_datetime

    @staticmethod
    def datetime_to_string(datetime: datetime):
        return datetime.strftime("%Y%m%d%H%M")

    @staticmethod
    def is_convertible(text):
        try:
            datetime.strptime(text, "%Y%m%d%H%M")
        except ValueError:
            return False
        return True
