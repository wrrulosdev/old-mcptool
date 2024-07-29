from loguru import logger
from mccolors import mcwrite

from ..commands.arguments.argument_validator import ValidateArgument
from ..constants import MCPToolStrings
from ..ipv4.get_cloudflare_ip import GetCloudflareIps
from ..scrappers.iphistory import DomainIPHistory
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'iphistory'
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

        if not ValidateArgument.is_domain(user_arguments[0]):
            mcwrite(Lm.get('errors.invalidDomain'))
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
        domain: str = user_arguments[0]

        # Execute the command
        ips: list = DomainIPHistory(domain=domain).get()

        if len(ips) == 0:
            mcwrite(Lm.get('commands.iphistory.noIpHistory'))
            return False

        cloudflare_ips: list = GetCloudflareIps().get(ips=ips)
        mcwrite(Lm.get('commands.iphistory.ipHistoryFound'))

        # Print the IP history (cloudflare ips)
        for ip in ips:
            if ip in cloudflare_ips:
                mcwrite(f'{MCPToolStrings.SPACES} &a&l• &d&l{ip} &8&l(&d&lCloudFlare&8&l)')

        # Print the IP history (non-cloudflare ips)
        for ip in ips:
            if ip not in cloudflare_ips:
                mcwrite(f'{MCPToolStrings.SPACES} &a&l• &f&l{ip}')

        return True
