import time

from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.dns.get_dns_records import GetDNSRecords
from mcptool.utilities.language.utilities import LanguageUtils as Lm
from mcptool.constants import MCPToolStrings


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'dnslookup'
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

        if not ValidateArgument.is_domain(user_arguments[0]):
            mcwrite(Lm.get('errors.invalidDomain'))
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
        domain: str = user_arguments[0]

        mcwrite(Lm.get(f'commands.{self.name}.lookingUp').replace('%domain%', domain))
        time.sleep(0.5)
        dns_records: list = GetDNSRecords(domain).get_dns_records()

        if len(dns_records) == 0:
            mcwrite(Lm.get(f'commands.{self.name}.noRecords'))
            return

        print('')

        for dns_record in dns_records:
            for value in dns_record['value']:
                mcwrite(f'{MCPToolStrings.SPACES}&4[&c&l{dns_record["type"]}&4] &f&l{value}')

        # Get the amount of DNS records found
        records_amount: int = len(dns_records)

        mcwrite(Lm.get(f'commands.{self.name}.done')
                .replace('%domain%', domain)
                .replace('%recordsAmount%', str(records_amount)
                         ))
