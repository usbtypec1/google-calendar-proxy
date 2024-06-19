from collections.abc import Iterable

from flask import Flask, request

import models
from credentials import load_unit_credentials
from services import (
    CalendarApiConnection,
    filter_already_started_events,
    filter_max_start_time,
)

app = Flask(__name__)


def map_events(events: Iterable[models.CalendarEvent]) -> list[dict]:
    return [
        {
            'id': event.id,
            'summary': event.summary,
            'start': {
                'dateTime': event.start.date_time.isoformat(),
                'timeZone': event.start.time_zone,
                'dateTimeUTC': event.start.date_time_utc.isoformat(),
            },
            'end': {
                'dateTime': event.end.date_time.isoformat(),
                'timeZone': event.end.time_zone,
                'dateTimeUTC': event.end.date_time_utc.isoformat(),
            },
        }
        for event in events
    ]


@app.get('/events')
def get_events():
    count = int(request.args.get('count', 10))
    calendar_id = request.args.get('calendar_id', 'primary')
    max_start_time_in_seconds = int(request.args.get(
        'max_start_time_in_seconds',
        60 * 60 * 24 * 2),
    )
    is_already_started_events_excluded = request.args.get(
        'is_already_started_events_excluded',
        True,
    )
    unit_id = request.args.get('unit_id')

    credentials = load_unit_credentials(unit_id)
    if credentials is None:
        return {'error': 'Credentials not found'}, 404

    events = CalendarApiConnection(credentials).get_events(
        max_results=count,
        calendar_id=calendar_id,
    )
    if is_already_started_events_excluded:
        events = filter_already_started_events(events)
    events = filter_max_start_time(
        max_start_time_in_seconds=max_start_time_in_seconds,
        events=events,
    )
    return map_events(events)
