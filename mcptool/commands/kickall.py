import time
from typing import Union

from loguru import logger
from mccolors import mcwrite

from ..commands.arguments.argument_validator import ValidateArgument
from ..minecraft.bot.server_response import BotServerResponse
from ..minecraft.server import JavaServerData, BedrockServerData
from ..minecraft.server.server_data import ServerData
from ..utilities.language.utilities import LanguageUtils as Lm
from ..utilities.minecraft.bot.utilities import BotUtilities


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'kickall'
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

        if not ValidateArgument.is_yes_no(user_arguments[2]):
            mcwrite(Lm.get('errors.invalidYesNo'))
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
        original_target: str = user_arguments[0]

        # Get the server data
        server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(target=original_target,
                                                                                 bot=False).get_data()
        if server_data is None:
            mcwrite(Lm.get('errors.serverOffline'))
            return False

        if server_data.platform != 'Java':
            mcwrite(Lm.get('errors.notJavaServer'))
            return False

        if ':' in user_arguments[0]:
            ip_address: str = original_target.split(':')[0]
            port: str = original_target.split(':')[1]

        else:
            ip_address: str = original_target
            port: str = str(server_data.port)

        version: str = user_arguments[1]
        loop: bool = user_arguments[2].lower() == 'y'

        # Execute the command
        mcwrite(Lm.get(f'commands.{self.name}.gettingPlayers').replace('%ip%', original_target))

        # Check if there are no players
        if len(server_data.player_list) == 0:
            mcwrite(Lm.get(f'commands.{self.name}.noPlayers').replace('%ip%', original_target))
            return True

        # Loop through the players and kick them
        for player in server_data.player_list:
            username: str = player['name']

            # Kick the player
            bot_response: str = BotServerResponse(ip_address=ip_address, port=int(port), version=version,
                                                  username=username).get_response()

            # Check if the player was kicked
            if bot_response == 'Connected':
                mcwrite(Lm.get('commands.kick.playerKicked')
                        .replace('%username%', username)
                        )

            else:
                # Get the bot color response
                bot_response: str = BotUtilities.get_bot_color_response(bot_response)

                mcwrite(Lm.get('commands.kick.playerNotKicked')
                        .replace('%username%', username)
                        .replace('%reason%', bot_response)
                        )

            time.sleep(BotUtilities.get_bot_reconnect_time())

        mcwrite(Lm.get(f'commands.{self.name}.allPlayersKicked'))

        # Check if the command should loop
        if loop:
            self.execute(user_arguments)

        return True
