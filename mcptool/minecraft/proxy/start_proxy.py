import datetime
import os
import subprocess

from mccolors import mcwrite
from ezjsonpy import get_config_value

from mcptool.constants import MCPToolStrings
from mcptool.path.mcptool_path import MCPToolPath
from mcptool.utilities.language.utilities import LanguageUtils as Lm
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
        mcwrite(Lm.get('commands.proxy.configuringProxy'))
        mcptool_path: str = MCPToolPath.get_path()

        if self.fakeproxy:
            self.proxy_path: str = f'{mcptool_path}/proxies/fakeproxy'
            self.proxy_port: int = get_config_value('fakeproxy.port', 'proxy')

        else:
            self.proxy_path: str = f'{mcptool_path}/proxies/velocity'
            self.proxy_port: int = get_config_value('velocity.port', 'proxy')

        original_proxy_settings_path: str = f'{mcptool_path}/settings/velocity.toml'
        proxy_settings_path: str = f'{self.proxy_path}/velocity.toml'

        if not os.path.exists(original_proxy_settings_path):
            mcwrite(Lm.get('errors.proxySettingsNotFound'))
            return

        # Read the original proxy settings file and replace the necessary values
        with open(original_proxy_settings_path, 'r') as file:
            proxy_settings: str = file.read()

        proxy_settings = proxy_settings.replace('[[ADDRESS]]', self.server)
        proxy_settings = proxy_settings.replace('[[PORT]]', str(self.proxy_port))
        proxy_settings = proxy_settings.replace('[[MODE]]', self.forwarding_mode)

        with open(proxy_settings_path, 'w') as file:
            file.write(proxy_settings)

        forwarding_secret_path: str = f'{self.proxy_path}/forwarding.secret'

        if not os.path.exists(forwarding_secret_path):  # Default forwarding secret
            with open(forwarding_secret_path, 'w') as file:
                file.write('CMsIjMYfQ27l')

        mcwrite(Lm.get('commands.proxy.proxyConfigured'))
        process: subprocess.Popen = self._start_proxy()

        if process is None:
            return

        self._read_output(process)

    def _read_output(self, process: subprocess.Popen) -> None:
        """
        Method to read the output of the proxy
        :param process: The proxy process
        """

        for line in process.stdout:
            try:
                output: str = line.decode('utf-8').strip()

            except UnicodeDecodeError:
                continue

            if output == '':
                continue

            if ' INFO]: Listening on ' in output:
                mcwrite(Lm.get('commands.proxy.proxyStarted')
                        .replace('%proxyIp%', '127.0.0.1')
                        .replace('%proxyPort%', str(self.proxy_port))
                        )

            if self.fakeproxy:
                current_time: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if ' [RFakeProxy] [CONNECTING] ' in output:
                    output_split: list = output.split(' ')
                    username: str = output_split[4]
                    ip_address: str = output_split[5]
                    mcwrite(Lm.get('commands.fakeproxy.connected')
                            .replace('%username%', username)
                            .replace('%ipAddress%', ip_address)
                            .replace('%time%', current_time)
                            )

                if ' [RFakeProxy] [DISCONNECTING] ' in output:
                    output_split: list = output.split(' ')
                    username: str = output_split[4]
                    ip_address: str = output_split[5]
                    mcwrite(Lm.get('commands.fakeproxy.disconnected')
                            .replace('%username%', username)
                            .replace('%ipAddress%', ip_address)
                            .replace('%time%', current_time)
                            )

                if ' [RFakeProxy] [CHAT] ' in output:
                    output_split: list = output.split(' ')
                    username: str = output_split[4]
                    ip_address: str = output_split[5]
                    message: str = ' '.join(output_split[6:])

                    if message.startswith('#send') or message.startswith('#help'):
                        continue

                    mcwrite(Lm.get('commands.fakeproxy.chat')
                            .replace('%username%', username)
                            .replace('%ipAddress%', ip_address)
                            .replace('%message%', message)
                            .replace('%time%', current_time)
                            )

                if ' [RFakeProxy] [COMMAND] ' in output:
                    output_split: list = output.split(' ')
                    username: str = output_split[4]
                    ip_address: str = output_split[5]
                    command: str = ' '.join(output_split[6:])
                    mcwrite(Lm.get('commands.fakeproxy.command')
                            .replace('%username%', username)
                            .replace('%ipAddress%', ip_address)
                            .replace('%command%', f'/{command}')
                            .replace('%time%', current_time)
                            )

                if ' [RFakeProxy] [ADMINKEY] ' in output:
                    mcwrite(Lm.get('commands.fakeproxy.adminKeyHelp').replace('%time%', current_time))
                    output_split: list = output.split(' ')
                    admin_key: str = output_split[4]
                    mcwrite(Lm.get('commands.fakeproxy.adminKey')
                            .replace('%adminKey%', admin_key)
                            .replace('%time%', current_time)
                            )

                if ' [RFakeProxy] [ADMIN] ' in output:
                    output_split: list = output.split(' ')
                    username: str = output_split[4]
                    ip_address: str = output_split[5]
                    mcwrite(Lm.get('commands.fakeproxy.adminKeyUsed')
                            .replace('%username%', username)
                            .replace('%ipAddress%', ip_address)
                            .replace('%time%', current_time)
                            )

                if ' [RFakeProxy] [SEND] ' in output:
                    output_split: list = output.split(' ')
                    sender: str = output_split[4]
                    ip_address: str = output_split[5]
                    target: str = output_split[6]
                    message: str = ' '.join(output_split[7:])
                    mcwrite(Lm.get('commands.fakeproxy.messageSent')
                            .replace('%sender%', sender)
                            .replace('%ipAddress%', ip_address)
                            .replace('%target%', target)
                            .replace('%message%', message)
                            .replace('%time%', current_time)
                            )

    def _start_proxy(self) -> subprocess.Popen:
        """
        Method to start the proxy
        :return: The proxy process
        """
        mcwrite(Lm.get('commands.proxy.startingProxy'))
        proxy_jar: str = 'fakeproxy' if self.fakeproxy else 'velocity'
        JarManager(
            jar_name=proxy_jar,
            jar_path=self.proxy_path
        ).check()
        command: str = f'cd {self.proxy_path} && java -jar {proxy_jar}.jar'

        if MCPToolStrings.OS_NAME == 'windows':
            command = f'C: && {command}'

        process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                     stderr=subprocess.STDOUT)
        return process
