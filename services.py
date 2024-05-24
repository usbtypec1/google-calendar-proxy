import logging
from zoneinfo import ZoneInfo
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

__all__ = ('get_events',)

logger = logging.getLogger(__name__)


def filter_max_start_time(
        *,
        events: list[dict],
        max_start_time_in_seconds: int,
) -> list[dict]:
    utc_now = datetime.now(ZoneInfo('UTC'))

    filtered = []

    for event in events:
        timezone = ZoneInfo(event['start']['timeZone'])
        start_time = datetime.fromisoformat(event['start']['dateTime'])
        start_time = start_time.astimezone(timezone)

        # if (utc_now - start_time).total_seconds() < max_start_time_in_seconds:
        #     continue

    return filtered


def get_events(
        *,
        calendar_id: str = 'primary',
        max_results: int = 10,
        credentials: Credentials,
):
    try:
        service = build(
            serviceName='calendar',
            version='v3',
            credentials=credentials,
        )

        now = f'{datetime.utcnow().isoformat()}Z'
        logger.info(f'Getting the upcoming {max_results} events')
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime',
            )
            .execute()
        )
        events = events_result.get('items', [])

        print(events)

        return events

    except HttpError as error:
        logger.exception(f'An error occurred', exc_info=error)


a = datetime.now(ZoneInfo('Asia/Yekaterinburg'))

print(a.astimezone(ZoneInfo('UTC')))