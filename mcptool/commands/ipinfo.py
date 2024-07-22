from typing import Union

from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.utilities.language.utilities import LanguageUtils as LM
from mcptool.ipv4.get_ip_info import IPInfo, IPInfoFormat


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'ipinfo'
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

        if not ValidateArgument.is_ip_address(user_arguments[0]):
            mcwrite(LM.get('errors.invalidIpFormat'))
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
        ip_address: str = user_arguments[0]

        # Execute the command
        mcwrite(LM.get(f'commands.{self.name}.gettingIpData'))
        ip_info: Union[IPInfoFormat, None] = IPInfo(ip_address=ip_address).get_info()

        if ip_info is None:
            mcwrite(LM.get(f'commands.{self.name}.error'))
            return

        mcwrite(LM.get(f'commands.{self.name}.continent').replace('%continent%', ip_info.continent).replace('%continentCode%', ip_info.continent_code))
        mcwrite(LM.get(f'commands.{self.name}.country').replace('%country%', ip_info.country).replace('%countryCode%', ip_info.country_code))
        mcwrite(LM.get(f'commands.{self.name}.region').replace('%region%', ip_info.region).replace('%regionName%', ip_info.region_name))
        mcwrite(LM.get(f'commands.{self.name}.city').replace('%city%', ip_info.city))
        mcwrite(LM.get(f'commands.{self.name}.timezone').replace('%timezone%', ip_info.timezone))
        mcwrite(LM.get(f'commands.{self.name}.isp').replace('%isp%', ip_info.isp))
        mcwrite(LM.get(f'commands.{self.name}.organization').replace('%organization%', ip_info.org))
