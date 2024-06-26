from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo

__all__ = (
    'CalendarEvent',
    'CalendarDateTime',
)


@dataclass
class CalendarDateTime:
    date_time: datetime
    time_zone: str

    @property
    def date_time_utc(self) -> datetime:
        return self.date_time.astimezone(ZoneInfo('UTC'))


@dataclass
class CalendarEvent:
    id: str
    start: CalendarDateTime
    end: CalendarDateTime
    summary: str = field(default='Без названия')
