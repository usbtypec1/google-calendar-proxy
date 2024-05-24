from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from google.oauth2.credentials import Credentials

from credentials import load_unit_credentials
from services import get_events

app = FastAPI()


def get_credentials(unit_id: str) -> Credentials:
    credentials = load_unit_credentials(unit_id)
    if credentials is None:
        raise HTTPException(status_code=404, detail="Credentials not found")
    return credentials


@app.get('/events')
def get_calendar_events(
        credentials: Credentials = Depends(get_credentials, use_cache=False),
        count: int = 100,
        calendar_id: str = 'primary',
):
    return get_events(
        credentials=credentials,
        max_results=count,
        calendar_id=calendar_id,
    )
