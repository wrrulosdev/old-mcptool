import os
import re
from typing import Union

from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.minecraft.server import JavaServerData, BedrockServerData
from mcptool.minecraft.server.server_data import ServerData
from mcptool.minecraft.server.show_server import ShowMinecraftServer
from mcptool.utilities.language.utilities import LanguageUtils as LM


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'checker'
        self.command_arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]
        self.servers_found: int = 0
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

        if not os.path.exists(user_arguments[0]):
            mcwrite(LM.get('errors.invalidFile'))
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
        file: str = user_arguments[0]

        # Execute the command
        with open(file, 'r') as f:
            lines: list = f.readlines()

        mcwrite(LM.get(f'commands.{self.name}.checking')
                .replace('%file%', file)
                )

        # Check the lines
        for line in lines:
            ips_and_ports: list = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)

            if len(ips_and_ports) == 0:
                continue

            for ip_and_port in ips_and_ports:
                server_data: Union[JavaServerData, BedrockServerData] = ServerData(target=ip_and_port).get_data()

                if server_data is not None:
                    ShowMinecraftServer.show(server_data=server_data)
                    self.servers_found += 1

        if self.servers_found == 0:
            mcwrite(LM.get(f'commands.{self.name}.noServersFound')
                    .replace('%file%', file)
                    )
            return

        mcwrite(LM.get(f'commands.{self.name}.serversFound')
                .replace('%servers%', str(self.servers_found))
                .replace('%file%', file)
                )
