import logging
import pathlib

from google.oauth2.credentials import Credentials

__all__ = (
    'load_all_credentials',
    'load_unit_credentials',
)

logger = logging.getLogger('tokens updater')


def load_all_credentials() -> dict[str, Credentials]:
    tokens_directory = pathlib.Path(__file__).parent / 'credentials'
    tokens_directory.mkdir(exist_ok=True)

    unit_id_to_credentials: dict[str, Credentials] = {}
    for token_file in tokens_directory.iterdir():
        if token_file.is_dir() or token_file.name == '.gitkeep':
            continue

        credentials = Credentials.from_authorized_user_file(str(token_file))
        unit_id_to_credentials[token_file.stem] = credentials

    return unit_id_to_credentials


def load_unit_credentials(unit_id: str) -> Credentials | None:
    tokens_directory = pathlib.Path(__file__).parent / 'credentials'
    tokens_directory.mkdir(exist_ok=True)

    token_file = tokens_directory / f'{unit_id}.json'
    if not token_file.exists():
        return
    return Credentials.from_authorized_user_file(str(token_file))
