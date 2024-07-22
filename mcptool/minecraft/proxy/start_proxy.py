import os
import subprocess

from mccolors import mcwrite
from ezjsonpy import get_config_value

from mcptool.constants import MCPToolStrings
from mcptool.path.mcptool_path import MCPToolPath
from mcptool.utilities.language.utilities import LanguageUtils as LM
from mcptool.minecraft.proxy.proxy_jar import JarManager


class StartProxy:
    def __init__(self, server: str, forwarding_mode: str, fakeproxy: bool = False) -> None:
        self.server = server
        self.forwarding_mode = forwarding_mode
        self.fakeproxy = fakeproxy
        self.proxy_path: str = ''
        self.proxy_port: int = 0

    def start(self) -> None:
        """Method to start the proxy"""
        self._configure_proxy()

    def _configure_proxy(self) -> None:
        """Method to configure the proxy"""
        mcptool_path: str = MCPToolPath.get_path()

        if self.fakeproxy:
            self.proxy_path: str = f'{mcptool_path}/proxies/fakeproxy'
            self.proxy_port: int = get_config_value('fakeproxy.port', 'proxy')

        else:
            self.proxy_path: str = f'{mcptool_path}/proxies/velocity'
            self.proxy_port: int = get_config_value('velocity.port', 'proxy')

        original_proxy_settings_path: str = f'{mcptool_path}/txt/velocity.toml'
        proxy_settings_path: str = f'{self.proxy_path}/velocity.toml'

        if not os.path.exists(original_proxy_settings_path):
            mcwrite(LM.get('errors.proxySettingsNotFound'))
            return

        # Read the original proxy settings file and replace the necessary values
        with open(original_proxy_settings_path, 'r') as file:
            proxy_settings: str = file.read()

        for line in proxy_settings.split('\n'):
            if 'bind = "' in line:
                proxy_settings = proxy_settings.replace(line, f'bind = "0.0.0.0:{self.proxy_port}"')

            if 'player-info-forwarding-mode = "' in line:
                proxy_settings = proxy_settings.replace(line, f'player-info-forwarding-mode = "{self.forwarding_mode}"')

            if 'lobby = "' in line:
                proxy_settings = proxy_settings.replace(line, f'lobby = "{self.server}"')

        with open(proxy_settings_path, 'w') as file:
            file.write(proxy_settings)

        print('Proxy configured successfully')
        self._start_proxy()

    def _start_proxy(self) -> subprocess.Popen:
        """Method to start the proxy"""
        proxy_jar: str = 'fakeproxy' if self.fakeproxy else 'velocity'
        JarManager(
            jar_name=proxy_jar,
            jar_path=self.proxy_path
        )
        command: str = f'cd {self.proxy_path} && java -jar velocity.jar'

        if MCPToolStrings.OS_NAME == 'windows':
            command = f'C: && {command}'

        process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return process
