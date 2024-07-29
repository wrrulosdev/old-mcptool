from typing import Union

from loguru import logger
from mccolors import mcwrite

from ..commands.arguments.argument_validator import ValidateArgument
from ..minecraft.server import JavaServerData, BedrockServerData
from ..minecraft.server.server_data import ServerData
from ..minecraft.server.show_server import ShowMinecraftServer
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'server'
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

        return True

    @logger.catch
    def execute(self, user_arguments: list) -> bool:
        """
        Method to execute the command
        :param user_arguments: list: The arguments to execute the command
        """
        if not self.validate_arguments(user_arguments):
            return False

        # Save user arguments
        server: str = user_arguments[0]
        # Execute the command
        mcwrite(Lm.get(f'commands.{self.name}.gettingServerData'))
        server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(server).get_data()

        if server_data is None:
            mcwrite(Lm.get('errors.serverOffline'))
            return True

        ShowMinecraftServer.show(server_data=server_data)
        return True
