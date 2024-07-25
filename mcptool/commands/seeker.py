from loguru import logger

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.utilities.language.utilities import LanguageUtils as Lm
from mcptool.utilities.seeker.utilities import SeekerUtilities


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'seeker'
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

        if not ValidateArgument.is_seeker_subcommand(user_arguments[0]):
            print('invalid sub command')
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
        sub_command: str = user_arguments[0]

        # Execute the command
        if sub_command == 'token':
            SeekerUtilities().get_token()

        if sub_command == 'servers':
            SeekerUtilities().get_servers()
