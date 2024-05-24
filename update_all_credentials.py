import logging

from google.auth import exceptions
from google.auth.transport.requests import Request

from credentials import load_all_credentials

logger = logging.getLogger('credentials updater')


def main() -> None:
    for unit_id, credentials in load_all_credentials().items():
        try:
            credentials.refresh(Request())
        except exceptions.RefreshError as error:
            logger.exception(
                f'Could not update credentials for unit={unit_id}',
                exc_info=error,
            )
        else:
            logger.info(f'Updated credentials for unit={unit_id}')


if __name__ == '__main__':
    main()
