import logging
from collections.abc import Iterable
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import models

__all__ = (
    'CalendarApiConnection',
    'filter_already_started_events',
    'filter_max_start_time',
)

logger = logging.getLogger(__name__)


def map_event(event: dict) -> models.CalendarEvent:
    return models.CalendarEvent(
        id=event['id'],
        summary=event['summary'],
        start=models.CalendarDateTime(
            date_time=datetime.fromisoformat(event['start']['dateTime']),
            time_zone=event['start']['timeZone'],
        ),
        end=models.CalendarDateTime(
            date_time=datetime.fromisoformat(event['end']['dateTime']),
            time_zone=event['end']['timeZone'],
        ),
    )


def map_events(events: Iterable[dict]) -> list[models.CalendarEvent]:
    return [map_event(event) for event in events]


def get_utc_now() -> datetime:
    return datetime.now(ZoneInfo('UTC'))


def filter_already_started_events(
        events: Iterable[models.CalendarEvent],
) -> list[models.CalendarEvent]:
    utc_now = get_utc_now()
    return [
        event for event in events
        if event.start.date_time_utc >= utc_now
    ]


def filter_max_start_time(
        *,
        max_start_time_in_seconds: int,
        events: Iterable[models.CalendarEvent],
) -> list[models.CalendarEvent]:
    utc_now = datetime.now(ZoneInfo('UTC'))

    filtered: list[models.CalendarEvent] = []
    for event in events:
        time_before_event_starts = event.start.date_time_utc - utc_now
        if time_before_event_starts.total_seconds() < max_start_time_in_seconds:
            filtered.append(event)
    return filtered


class CalendarApiConnection:

    def __init__(self, credentials: Credentials):
        self.__calendar_service = build(
            serviceName='calendar',
            version='v3',
            credentials=credentials,
        )

    def get_events(
            self,
            calendar_id: str = 'primary',
            max_results: int = 10,
    ) -> list[models.CalendarEvent]:
        now = f'{datetime.utcnow().isoformat()}Z'
        logger.info(f'Getting the upcoming {max_results} events')

        try:
            events_result = (
                self.__calendar_service
                .events()
                .list(
                    calendarId=calendar_id,
                    timeMin=now,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy='startTime',
                )
                .execute()
            )

        except HttpError as error:
            logger.exception(f'An error occurred', exc_info=error)
            raise HTTPException(
                status_code=error.status_code,
                detail=str(error),
            )

        events = events_result.get('items', [])
        return map_events(events)
