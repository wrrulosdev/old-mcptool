from typing import Union

from loguru import logger
from mccolors import mcreplace, mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.utilities.language.utilities import LanguageUtils as Lm


class Input:
    def __init__(self, input_message: Union[str, None], input_type: str) -> None:
        """
        Initialize the Input class
        :param input_message: str: The inputcustom message
        :param input_type: str: The inputcustom type
        """
        self.input_message: Union[str, None] = input_message
        self.input_type: str = input_type
        self.user_input: str = ''

    @logger.catch
    def get_input(self) -> Union[str, int, bool, None]:
        """
        Method to get the user inputcustom and validate it
        :return: Value of the user inputcustom or None if the inputcustom is invalid
        """
        # Check if the inputcustom message is None
        if self.input_message is None:
            logger.error('Input message in Input class is None')
            return None

        output: Union[tuple, None] = None

        while True:
            try:
                # Get the user inputcustom
                self.user_input: str = input(mcreplace(self.input_message))

                if self.input_type == 'string':
                    return self._string_input()

                if self.input_type == 'integer':
                    output: Union[int, None] = self._integer_input()

                if self.input_type == 'boolean':
                    output: Union[bool, None] = self._boolean_input()

                if self.input_type == 'country_code':
                    output: Union[str, None] = self._country_code_input()

                if self.input_type == 'velocity_forwarding_mode':
                    output: Union[str, None] = self._velocity_forwarding_mode_input()

                if output is not None:
                    return output

            except (KeyboardInterrupt, EOFError):
                print('')  # Print a new line
                return None

    @logger.catch
    def _string_input(self) -> str:
        """Get the string inputcustom"""
        return self.user_input

    @logger.catch
    def _integer_input(self) -> Union[int, None]:
        """Get the integer inputcustom"""
        try:
            return int(self.user_input)
        except ValueError:
            mcwrite(Lm.get('errors.invalidIntgerInput'))
            return None

    @logger.catch
    def _boolean_input(self) -> Union[bool, None]:
        """Get the boolean inputcustom"""
        if self.user_input.lower() in ['yes', 'y', 'true', '1']:
            return True

        if self.user_input.lower() in ['no', 'n', 'false', '0']:
            return False

        mcwrite(Lm.get('errors.invalidBooleanInput'))
        return None

    @logger.catch
    def _country_code_input(self) -> Union[str, None]:
        """Get the country code inputcustom"""
        if len(self.user_input) == 2:
            return self.user_input

        mcwrite(Lm.get('errors.invalidCountryCodeInput'))
        return None

    @logger.catch
    def _velocity_forwarding_mode_input(self) -> Union[str, None]:
        """Get the velocity forwarding mode inputcustom"""
        if ValidateArgument.is_velocity_forwading_mode(self.user_input):
            return self.user_input

        mcwrite(Lm.get('errors.invalidVelocityForwardingModeInput'))
        return None
