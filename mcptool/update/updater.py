import requests
from loguru import logger

from .. import URLS, MCPToolStrings


class Updater:
    @staticmethod
    @logger.catch
    def update_available() -> bool:
        """
        Check if an update is available
        :return: True if an update is available, False otherwise
        """
        try:
            response: requests.Response = requests.get(f'{URLS.RAW_GITHUB_REPOSITORY}/settings/settings.json')

            if response.status_code != 200:
                return False

            settings = response.json()
            return settings['version'] != MCPToolStrings.VERSION

        except Exception as e:
            logger.warning(f'Error checking for updates: {e}')
            return False
