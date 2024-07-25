import os
import subprocess
from typing import Union

from loguru import logger
from mccolors import mcwrite

from mcptool import MCPToolPath
from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.constants import MCPToolStrings
from mcptool.minecraft.server import JavaServerData, BedrockServerData
from mcptool.minecraft.server.server_data import ServerData
from mcptool.utilities.language.utilities import LanguageUtils as LM
from mcptool.ipv4.get_ip_info import IPInfo, IPInfoFormat


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'sendcmd'
        self.command_arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]
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
            mcwrite(LM.get('errors.invalidServerFormat'))
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
            mcwrite(LM.get('errors.serverOffline'))
            return

        if server_data.platform != 'Java':
            mcwrite(LM.get('errors.notJavaServer'))
            return

        if ':' in user_arguments[0]:
            ip_address: str = original_target.split(':')[0]
            port: str = original_target.split(':')[1]

        else:
            ip_address: str = original_target
            port: str = str(server_data.port)

        version: str = user_arguments[1]
        username: str = user_arguments[2]
        commands_file: str = user_arguments[3]

        # Execute the command
        mcwrite(LM.get(f'commands.{self.name}.gettingCommands').replace('%file%', commands_file))

        # Get absolute path of the commands file
        commands_file = os.path.abspath(commands_file)

        # Check if the commands file is empty
        with open(commands_file, 'r') as file:
            commands = file.read().splitlines()

        if len(commands) == 0:
            mcwrite(LM.get('errors.commandsFileEmpty'))
            return

        path: str = MCPToolPath.get_path()
        command: str = f'cd {path} && node scripts/sendcmd.mjs {ip_address} {port} {username} {version} {commands_file} {MCPToolStrings.SPACES}'

        if MCPToolStrings.OS_NAME == 'windows':
            command = f'C: && {command}'

        # Start sending the commands to the server
        mcwrite(LM.get(f'commands.{self.name}.sendingCommands')
                .replace('%ip%', f'{ip_address}:{port}')
                .replace('%username%', username)
                .replace('%commandsFile%', commands_file)
                .replace('%commands%', str(len(commands)))
                )
        subprocess.run(command, shell=True)
