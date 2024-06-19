import logging
import pathlib

from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger('Auth flow')

NAME = 'unit id'

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def load_installed_app_flow() -> InstalledAppFlow:
    oauth_flow_credentials_file_path = (
            pathlib.Path(__file__).parent
            / 'oauth_credentials'
            / f'{NAME}_credentials.json'
    )
    if not oauth_flow_credentials_file_path.exists():
        logger.error('oauth_credentials.json not found')
        exit(0)
    return InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=str(oauth_flow_credentials_file_path),
        scopes=SCOPES,
    )


def start_auth_flow(installed_app_flow: InstalledAppFlow) -> None:
    file_path = (
            pathlib.Path(__file__).parent
            / 'credentials'
            / f'{NAME}.json'
    )
    credentials = installed_app_flow.run_local_server(port=0)
    file_path.write_text(credentials.to_json(), encoding='utf-8')
    logger.info(f'Credentials saved to {file_path}')


def main() -> None:
    installed_app_flows = load_installed_app_flow()
    start_auth_flow(installed_app_flows)


if __name__ == '__main__':
    main()
