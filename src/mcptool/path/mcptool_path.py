import os
import subprocess
from typing import Union

import requests
from loguru import logger
from mccolors import mcwrite, mcreplace

from ..constants import URLS, MCPToolStrings


class MCPToolPath:
    def __init__(self) -> None:
        self.files = self._get_mcptool_files()
        self.check_files()

    @staticmethod
    @logger.catch
    def get_path() -> str:
        """
        Get the path to the MCPToolFiles folder
        :return: str: The path to the MCPToolFiles folder
        """
        folder_name: str = 'MCPToolFiles'

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
                mcwrite(f'&8&l[&a&lINFO&8&l] &f&lDownloading {str(file.file_path)}...')
                logger.info(f'Downloading {str(file.file_path)}')
                file.download()

        if not os.path.exists(os.path.join(self.get_path(), 'node_modules')):
            logger.info('Installing node modules')
            mcwrite('&8&l[&a&lINFO&8&l] &f&lInstalling node modules...')
            command: str = f'cd {self.get_path()} && npm install'

            if MCPToolStrings.OS_NAME == 'windows':
                command = f'C: && {command}'

            error: Union[bytes, None] = subprocess.run(command, shell=True, capture_output=True).stderr

            if error:
                error_str: str = error.decode('utf-8').strip()
                mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError installing node modules: {error_str}')
                logger.error(f'Error installing node modules: {error_str}')

    @logger.catch
    def _get_mcptool_files(self) -> list:
        """
        Get the URL files
        :return: list: The MCPTool files
        """
        return [
            # Settings
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/settings.json',
                file_name='settings/settings.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/nordify.json',
                file_name='settings/nordify.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/scanner.json',
                file_name='settings/scanner.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/proxy.json',
                file_name='settings/proxy.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/mcserver-scrapper.json',
                file_name='settings/mcserver-scrapper.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/bruteforce_settings.json',
                file_name='settings/bruteforce_settings.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/sendcmd_settings.json',
                file_name='settings/sendcmd_settings.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/settings/velocity.toml',
                file_name='settings/velocity.toml'
            ),
            # Languages
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/languages/en.json',
                file_name='languages/en.json'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/languages/es.json',
                file_name='languages/es.json'
            ),
            # Jars
            MCPToolFile(
                download_url=f'{URLS.RFAKEPROXY_JAR_URL}',
                file_name='proxies/fakeproxy/plugins/RFakeProxy.jar'
            ),
            MCPToolFile(
                download_url=f'{URLS.MCPTOOL_VELOCITY_JAR_URL}',
                file_name='proxies/velocity/plugins/MCPTool.jar'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/scanners/qubo.jar',
                file_name='scanners/qubo.jar'
            ),
            # Scripts (.mjs)
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/scripts/bot.mjs',
                file_name='scripts/bot.mjs'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/scripts/brute_auth.mjs',
                file_name='scripts/brute_auth.mjs'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/scripts/connect.mjs',
                file_name='scripts/connect.mjs'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/scripts/sendcmd.mjs',
                file_name='scripts/sendcmd.mjs'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/scripts/server_response.mjs',
                file_name='scripts/server_response.mjs'
            ),
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/scripts/utilities.mjs',
                file_name='scripts/utilities.mjs'
            ),
            # Packages
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/package.json',
                file_name='package.json'
            ),
            # Images
            MCPToolFile(
                download_url=f'{URLS.RAW_GITHUB_REPOSITORY}/files/img/icon.ico',
                file_name='files/img/icon.ico'
            ),
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
                input(mcreplace('&8&l[&c&lERROR&8&l] &f&lPress enter to continue...'))
                return

            with open(self.file_path, 'wb') as file:
                if response.content is None:
                    mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError downloading file: {self.file_path} (No content)')
                    logger.error(f'Error downloading {self.download_url}')
                    input(mcreplace('&8&l[&c&lERROR&8&l] &f&lPress enter to continue...'))
                    return

                file.write(response.content)

        except requests.exceptions.RequestException as e:
            mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError downloading file: {self.file_path} ({e})')
            logger.error(f'Error downloading {self.download_url}')
