from typing import Annotated

from fastapi import APIRouter, Depends, Query

import models
from dependencies import get_calendar_api_connection
from services import (
    CalendarApiConnection, filter_already_started_events,
    filter_max_start_time,
)

router = APIRouter(prefix='/events', tags=['Events'])


@router.get('', response_model=list[models.CalendarEvent])
def get_calendar_events(
        calendar_api_connection: Annotated[
            CalendarApiConnection,
            Depends(get_calendar_api_connection),
        ],
        count: Annotated[
            int,
            Query(
                ge=1,
                description='Максимальное количество событий для получения',
            )
        ] = 10,
        calendar_id: Annotated[
            str,
            Query(description=(
                    'ID календаря.'
                    ' По умолчанию события берутся из основного календаря'
            ))
        ] = 'primary',
        max_start_time_in_seconds: Annotated[
            int,
            Query(
                description=(
                        'Событие не должно начаться позже текущего времени'
                        ' + ЭТО указанное время.'
                        ' Например, если указать 3600 секунд,'
                        ' то вы получите события только за следующий час.'
                        ' По умолчанию 2 дня.'
                ),
            ),
        ] = 60 * 60 * 24 * 2,
        is_already_started_events_excluded: Annotated[
            bool,
            Query(description='Исключить события, которые уже начались'),
        ] = True,
):
    events = calendar_api_connection.get_events(
        max_results=count,
        calendar_id=calendar_id,
    )
    events = filter_max_start_time(
        max_start_time_in_seconds=max_start_time_in_seconds,
        events=events,
    )
    if is_already_started_events_excluded:
        events = filter_already_started_events(events)
    return events
