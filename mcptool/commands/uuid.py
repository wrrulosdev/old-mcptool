import uuid

from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.minecraft.player.get_player_uuid import PlayerUUID
from mcptool.minecraft.player.get_player_username import PlayerUsername
from mcptool.utilities.language.utilities import LanguageUtils as LM


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'uuid'
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
        username: str = user_arguments[0]

        # Execute the command
        # Check if the username is a UUID with dashes
        if len(username) == 36:
            username = username.replace('-', '')

        # if the username is a UUID
        if len(username) == 32:
            mcwrite(f"{LM.get(f'commands.{self.name}.gettingPlayerUsername')}")
            player_data = PlayerUsername(uuid=username).get_username()

            if player_data is None:
                mcwrite(f"{LM.get(f'commands.{self.name}.playerNotFound')}")
                return

            mcwrite(LM.get(f'commands.{self.name}.username').replace('%username%', f'&a&l{player_data}'))
            return

        # if the username is a simple username
        mcwrite(f"{LM.get(f'commands.{self.name}.gettingPlayerUuid')}")
        player_data = PlayerUUID(username=username).get_uuid()
        print('')
        if player_data.online_uuid is not None:
            mcwrite(LM.get(f'commands.{self.name}.uuid')
                    .replace('%uuid%', f'&a&l{player_data.online_uuid}')
                    .replace('%uuidVariant%', f'&a&l{uuid.UUID(player_data.online_uuid)}')
                    )

        mcwrite(LM.get(f'commands.{self.name}.uuid')
                .replace('%uuid%', f'&c&l{player_data.offline_uuid}')
                .replace('%uuidVariant%', f'&c&l{uuid.UUID(player_data.offline_uuid)}')
                )
