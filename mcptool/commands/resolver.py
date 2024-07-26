import time

from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.constants import MCPToolStrings
from mcptool.ipv4.get_cloudflare_ip import GetCloudflareIps
from mcptool.utilities.language.utilities import LanguageUtils as Lm
from mcptool.hackertarget.get_subdomains import GetSubdomains as GetSubdomainsHackerTarget
from mcptool.virustotal.get_subdomains import GetSubdomains as GetSubdomainsVirustotal


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'resolver'
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
            mcwrite(Lm.get('errors.invalidIpFormat').replace('%ip%', user_arguments[0]))
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
        mcwrite(Lm.get(f'commands.{self.name}.resolving').replace('%domain%', domain))
        time.sleep(0.5)

        # Get the subdomains of the domain using VirusTotal API
        mcwrite(Lm.get(f'commands.{self.name}.gettingSubdomainsVirusTotal'))
        subdomains_virustotal: list = GetSubdomainsVirustotal().get_subdomains(domain=domain)

        # Get the subdomains of the domain using HackerTarget API
        mcwrite(Lm.get(f'commands.{self.name}.gettingSubdomainsHackerTarget'))
        subdomains_hackertarget: list = GetSubdomainsHackerTarget().get_subdomains(domain=domain)

        # Merge the subdomains
        subdomains: list = subdomains_virustotal + subdomains_hackertarget

        # Remove duplicates
        temp_dict = {}

        for item in subdomains:
            temp_dict[item[1]] = item

        # Get the subdomains list without duplicates
        subdomains_list = list(temp_dict.values())

        if len(subdomains_list) == 0:
            mcwrite(Lm.get('errors.noSubdomainsFoundResolver'))
            return False

        # Get ips from the subdomains
        ips = [subdomain[1] for subdomain in subdomains_list]

        # Get Cloudflare IPs from the list of IPs
        cloudflare_ips = GetCloudflareIps().get(ips=ips)
        print('')

        # Print the subdomains with the cloudflare ips
        for subdomain, ip in subdomains_list:
            if ip in cloudflare_ips:
                mcwrite(f'{MCPToolStrings.SPACES} &a&l• &d&l{ip} &8&l(&a&l{subdomain}&8&l) &8&l(&d&lCloudFlare&8&l)')

        # Print the subdomains with unknown ips
        for subdomain, ip in subdomains_list:
            if ip not in cloudflare_ips:
                mcwrite(f'{MCPToolStrings.SPACES} &a&l• &f&l{ip} &8&l(&a&l{subdomain}&8&l)')

        mcwrite(Lm.get(f'commands.{self.name}.done')
                .replace('%domain%', domain)
                .replace('%subdomainsAmount%', str(len(subdomains_list))
                         ))
        return True
