from datetime import datetime, timezone
from pydantic import BaseConfig, BaseModel
from typing import Optional
# from dateutil import tz

# FRA = tz.gettz('Europe/Paris')

class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }


class DateTimeModel(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class DBModelMixin(DateTimeModel):
    id: Optional[int] = None