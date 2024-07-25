import time
from typing import Union

from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.minecraft.bot.server_response import BotServerResponse
from mcptool.minecraft.server import JavaServerData, BedrockServerData
from mcptool.minecraft.server.server_data import ServerData
from mcptool.utilities.language.utilities import LanguageUtils as Lm
from mcptool.utilities.minecraft.bot.utilities import BotUtilities


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'kick'
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

        if not ValidateArgument.is_yes_no(user_arguments[3]):
            mcwrite(LM.get('errors.invalidYesNo'))
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
        loop: bool = user_arguments[3].lower() == 'y'

        # Execute the command
        mcwrite(Lm.get(f'commands.{self.name}.kickingPlayer')
                .replace('%ip%', original_target)
                .replace('%version%', version)
                .replace('%username%', username)
                )

        # Kick the player
        bot_response: str = BotServerResponse(ip_address=ip_address, port=int(port), version=version,
                                              username=username).get_response()

        # Check if the player was kicked
        if bot_response == 'Connected':
            mcwrite(Lm.get(f'commands.{self.name}.playerKicked')
                    .replace('%username%', username)
                    )

        else:
            # Get the bot color response
            bot_response: str = BotUtilities.get_bot_color_response(bot_response)

            mcwrite(Lm.get(f'commands.{self.name}.playerNotKicked')
                    .replace('%username%', username)
                    .replace('%reason%', bot_response)
                    )

        if loop:
            time.sleep(BotUtilities.get_bot_reconnect_time())
            self.execute(user_arguments)
