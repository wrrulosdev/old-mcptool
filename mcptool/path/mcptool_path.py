import os
from typing import Union

import requests
from loguru import logger
from mccolors import mcwrite

from mcptool.constants import URLS


class MCPToolPath:
    def __init__(self) -> None:
        self.files = self._get_mcptool_files()
        self.check_files()

    @staticmethod
    @logger.catch
    def get_path() -> str:
        """
        Get the path to the MCPToolData folder
        :return: str: The path to the MCPToolData folder
        """
        folder_name: str = 'MCPToolData'

        if os.name == 'nt':
            path: str = os.path.abspath(os.path.join(os.getenv('APPDATA'), folder_name))

        else:
            path: str = os.path.abspath(os.path.join(os.getenv('HOME'), '.config', folder_name))

        if not os.path.exists(path):
            logger.info(f'Creating MCPTool folder in {path}')
            os.makedirs(os.path.join(path), exist_ok=True)

        return path

    @logger.catch
    def check_files(self) -> None:
        """Check if the files exist and download them if they don't"""
        for file in self.files:
            if not os.path.exists(file.file_path):
                logger.info(f'Downloading {file.file_path}')
                file.download()

    @logger.catch
    def _get_mcptool_files(self) -> list:
        """
        Get the URL files
        :return: list: The MCPTool files
        """

        return [
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/settings.json',
                file_name='settings/settings.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/proxy.json',
                file_name='settings/proxy.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/velocity.toml',
                file_name='settings/velocity.toml'
            )
        ]


class MCPToolFile:
    def __init__(self, download_url: Union[str, None] = None, file_name: Union[str, None] = None):
        self.download_url = download_url
        self.file_path = os.path.abspath(os.path.join(MCPToolPath.get_path(), file_name))

    @logger.catch
    def download(self) -> None:
        """Download the file"""
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        try:
            response: requests.Response = requests.get(self.download_url)

            if response.status_code != 200:
                mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError downloading file: {self.file_path} ({response.status_code})')
                logger.error(f'Error downloading {self.download_url}')
                return

            with open(self.file_path, 'wb') as file:
                if response.content is None:
                    mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError downloading file: {self.file_path} (No content)')
                    logger.error(f'Error downloading {self.download_url}')
                    return

                file.write(response.content)

        except requests.exceptions.RequestException as e:
            mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError downloading file: {self.file_path} ({e})')
            logger.error(f'Error downloading {self.download_url}')
