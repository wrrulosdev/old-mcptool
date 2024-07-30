from ezjsonpy import get_config_value, set_config_value, set_language
from loguru import logger
from mccolors import mcwrite

from ..commands.arguments.argument_validator import ValidateArgument
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'language'
        self.command_arguments: list = [i for i in Lm.get(f'commands.{self.name}.arguments')]

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

        if not ValidateArgument.is_valid_language(user_arguments[0]):
            mcwrite(Lm.get('errors.invalidLanguage'))
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
        language_name: str = user_arguments[0]

        # Execute the command
        if get_config_value('language') == language_name:
            mcwrite(Lm.get(f'commands.{self.name}.sameLanguage').replace('%language%', language_name))
            return False

        set_config_value('language', language_name)
        set_language(language_name)
        mcwrite(Lm.get(f'commands.{self.name}.languageChanged').replace('%language%', language_name))
        return True
