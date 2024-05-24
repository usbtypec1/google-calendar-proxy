from typing import Annotated

from fastapi import Depends, Query
from fastapi.exceptions import HTTPException
from google.oauth2.credentials import Credentials

from credentials import load_unit_credentials
from services import CalendarApiConnection

__all__ = (
    'get_credentials',
    'get_calendar_api_connection',
)


def get_credentials(
        unit_id: Annotated[str, Query(description='ID пиццерии')],
) -> Credentials:
    credentials = load_unit_credentials(unit_id)
    if credentials is None:
        raise HTTPException(status_code=404, detail="Credentials not found")
    return credentials


def get_calendar_api_connection(
        credentials: Annotated[Credentials, Depends(get_credentials)],
) -> CalendarApiConnection:
    return CalendarApiConnection(credentials)
