import time
from typing import Union

from loguru import logger
from mccolors import mcwrite

from ..commands.arguments.argument_validator import ValidateArgument
from ..minecraft.player.get_player_uuid import PlayerUUID
from ..minecraft.server import JavaServerData, BedrockServerData
from ..minecraft.server.server_data import ServerData
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'listening'
        self.command_arguments: list = [i for i in Lm.get(f'commands.{self.name}.arguments')]
        self.players: list = []
        self.attempts: int = 0
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
        mcwrite(Lm.get(f'commands.{self.name}.connecting').replace('%ip%', server))

        # Get the server data
        server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(target=server,
                                                                                 bot=False).get_data()

        if server_data is None:
            mcwrite(Lm.get('errors.serverOffline'))
            return False

        if server_data.platform != 'Java':
            mcwrite(Lm.get('errors.notJavaServer'))
            return False

        mcwrite(Lm.get(f'commands.{self.name}.waitingForConnections').replace('%ip%', server))

        while True:
            server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(target=server,
                                                                                     bot=False).get_data()
            # Check if the server is offline
            if server_data is None:
                self.attempts += 1
                time.sleep(30)
                continue

            # Check if the server has players
            if len(server_data.player_list) == 0:
                continue

            for player in server_data.player_list:
                # If there are no players, print the message
                if len(self.players) == 0:
                    mcwrite(Lm.get(f'commands.{self.name}.playersFound'))

                if player not in self.players:
                    self.players.append(player)

                    if player['id'] is None:
                        continue

                    if player['id'] == '00000000-0000-0000-0000-000000000000':
                        continue

                    uuid_color: str = PlayerUUID(username=player['name']).get_uuid_color(player['id'])
                    mcwrite(Lm.get(f'commands.{self.name}.playerFoundFormat')
                            .replace('%username%', player['name'])
                            .replace('%uuid%', f"{uuid_color}{player['id']}")
                            )

            time.sleep(1)

        return True
