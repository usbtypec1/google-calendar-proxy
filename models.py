from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import AwareDatetime, BaseModel, Field, computed_field

__all__ = (
    'CalendarEvent',
    'CalendarDateTime',
)


class CalendarDateTime(BaseModel):
    date_time: Annotated[
        AwareDatetime,
        Field(
            alias='dateTime',
            description='Дата и время начала события в локальном часовом поясе',
        ),
    ]
    time_zone: Annotated[
        str,
        Field(alias='timeZone', description='Часовой пояс'),
    ]

    @computed_field(
        alias='dateTimeUTC',
        description='Дата и время начала события в UTC',
    )
    @property
    def date_time_utc(self) -> AwareDatetime:
        return self.date_time.astimezone(ZoneInfo('UTC'))


class CalendarEvent(BaseModel):
    id: Annotated[str, Field(description='ID события')]
    summary: Annotated[
        str,
        Field(
            default='Без названия',
            description='Название события',
        ),
    ]
    start: Annotated[
        CalendarDateTime,
        Field(description='Дата и время начала события'),
    ]
    end: Annotated[
        CalendarDateTime,
        Field(description='Дата и время окончания события'),
    ]
