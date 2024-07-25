import subprocess
from typing import Union

from loguru import logger
from mccolors import mcwrite

from mcptool import MCPToolPath
from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.constants import MCPToolStrings, CLI
from mcptool.minecraft.server import JavaServerData, BedrockServerData
from mcptool.minecraft.server.server_data import ServerData
from mcptool.utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'connect'
        self.command_arguments: list = [i for i in Lm.get(f'commands.{self.name}.arguments')]
        logger.debug(f"Command initialized: {self.name}, arguments: {self.command_arguments}")

    @logger.catch
    def validate_arguments(self, user_arguments: list) -> bool:
        """
        Method to validate the arguments
        :param user_arguments: list: The arguments to validate
        :return: bool: True if the arguments are valid, False otherwise
        """
        if not ValidateArgument.validate_arguments_length(
                command_name=self.name,
                command_arguments=self.command_arguments,
                user_arguments=user_arguments
        ):
            return False

        if not ValidateArgument.is_domain(domain=user_arguments[0]) and not ValidateArgument.is_ip_and_port(
                ip=user_arguments[0]) and not ValidateArgument.is_domain_and_port(domain=user_arguments[0]):
            mcwrite(Lm.get('errors.invalidServerFormat'))
            return False

        return True

    @logger.catch
    def execute(self, user_arguments: list) -> None:
        """
        Method to execute the command
        :param user_arguments: list: The arguments to execute the command
        """
        if not self.validate_arguments(user_arguments):
            return

        # Save user arguments
        original_target: str = user_arguments[0]

        # Get the server data
        server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(target=original_target,
                                                                                 bot=False).get_data()

        if server_data is None:
            mcwrite(Lm.get('errors.serverOffline'))
            return

        if server_data.platform != 'Java':
            mcwrite(Lm.get('errors.notJavaServer'))
            return

        if ':' in user_arguments[0]:
            ip_address: str = original_target.split(':')[0]
            port: str = original_target.split(':')[1]

        else:
            ip_address: str = original_target
            port: str = str(server_data.port)

        version: str = user_arguments[1]
        username: str = user_arguments[2]
        path: str = MCPToolPath.get_path()
        spaces: str = '0' if CLI.value else MCPToolStrings.SPACES
        command: str = f'cd {path} && node scripts/connect.mjs {ip_address} {port} {username} {version} {spaces}'

        if MCPToolStrings.OS_NAME == 'windows':
            command = f'C: && {command}'

        # Connecting to the server
        mcwrite(Lm.get(f'commands.{self.name}.connecting')
                .replace('%ip%', ip_address)
                .replace('%username%', username)
                )
        subprocess.run(command, shell=True)
