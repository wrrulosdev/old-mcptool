import json
import os
import subprocess

from ezjsonpy import remove_configuration, load_configuration
from loguru import logger
from mccolors import mcwrite

from .. import MCPToolPath
from ..commands.arguments.argument_validator import ValidateArgument
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'settings'
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

        if not ValidateArgument.is_valid_settings_name(user_arguments[0]):
            mcwrite(Lm.get('errors.invalidSettingName'))
            return False

        if os.name != 'nt':
            mcwrite(Lm.get('errors.windowsOnly'))
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
        setting_name: str = user_arguments[0]

        # Execute the command
        if setting_name != 'velocity':
            settings_path: str = f'{MCPToolPath.get_path()}/settings/{setting_name}.json'

        else:
            settings_path: str = f'{MCPToolPath.get_path()}/settings/{setting_name}.toml'

        # Create settings backup
        with open(settings_path, 'r') as file:
            settings_backup: str = file.read()

        # Open the settings file with notepad
        subprocess.run(['notepad', settings_path])

        if setting_name in ['velocity', 'bruteforce_settings', 'sendcmd_settings', 'mcserver-scrapper']:
            mcwrite(Lm.get(f'commands.{self.name}.settingsUpdated'))
            return True

        # Validate the new settings
        with open(settings_path, 'r') as file:
            new_settings: str = file.read()

        try:
            json.loads(new_settings)

            # This is because the default settings file is named 'default' instead of 'settings'
            if setting_name == 'settings':
                setting_name = 'default'

            remove_configuration(setting_name)
            load_configuration(setting_name, settings_path)
            mcwrite(Lm.get(f'commands.{self.name}.settingsUpdated'))

        except json.JSONDecodeError:
            mcwrite(Lm.get('errors.invalidNewSettingsFile'))

            # Restore the settings
            with open(settings_path, 'w') as file:
                file.write(settings_backup)

        return True
