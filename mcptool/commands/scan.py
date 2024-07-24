import os
from typing import Union

from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.inputcustom import Input
from mcptool.nbt.servers_dat import ServersDAT
from mcptool.scanner.external_scanner import ExternalScanner
from mcptool.scanner.py_scanner import PyScanner
from mcptool.utilities.language.utilities import LanguageUtils as LM
from mcptool.utilities.scanner.utilities import ScannerUtilities


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'scan'
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

        if str(user_arguments[0]).endswith('.txt'):
            if not os.path.exists(user_arguments[0]):
                mcwrite(LM.get('errors.invalidFile'))
                return False

        if not ValidateArgument.is_scan_method(user_arguments[2]):
            mcwrite(LM.get('errors.invalidScanMethod'))
            return False

        # Validate the IP address and port range if the method is Python scanner
        if user_arguments[2] == 'py':
            if not str(user_arguments[0]).endswith('.txt'):
                if not ValidateArgument.is_ip_address(user_arguments[0]):
                    mcwrite(LM.get('errors.invalidIpFormat').replace('%ip%', user_arguments[0]))
                    return False

            if not ValidateArgument.is_port_range_py_method(user_arguments[1]):
                mcwrite(LM.get('errors.invalidPortRange'))
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
        target: str = user_arguments[0]
        port_range: str = user_arguments[1]
        method: str = user_arguments[2]

        if method != 'py':
            if method == 'nmap':
                if not ScannerUtilities.nmap_installed():
                    mcwrite(LM.get('errors.nmapNotInstalled'))
                    return

            if method == 'masscan':
                if not ScannerUtilities.masscan_installed():
                    mcwrite(LM.get('errors.masscanNotInstalled'))
                    return

        # Execute the command
        if target.endswith('.txt'):
            outputs: list[dict] = []
            with open(target, 'r') as file:
                for line in file:
                    target = line.strip()
                    output: Union[dict, None] = self.scan(target=target, port_range=port_range, method=method)
                    outputs.append(output)

            for output in outputs:
                self.show_output(output)

        else:
            output: Union[dict, None] = self.scan(target=target, port_range=port_range, method=method)
            self.show_output(output)

    @logger.catch
    def scan(self, target: str, port_range: str, method: str) -> Union[dict, None]:
        """
        Method to scanner the target
        :param target: str: The target to scanner
        :param port_range: str: The port range to scanner
        :param method: str: The method to scanner the target
        """
        if method == 'py':
            if not ValidateArgument.is_ip_address(target):
                mcwrite(LM.get('errors.invalidIpFormat').replace('%ip%', target))
                return None

        mcwrite(LM.get(f'commands.{self.name}.scanning')
                .replace('%ip%', target)
                .replace('%portRange%', port_range)
                .replace('%method%', method)
                )

        if method == 'py':
            output: Union[dict, None] = PyScanner(ip_address=target, port_range=port_range).scan()

        else:
            output: Union[dict, None] = ExternalScanner(target=target, port_range=port_range, scanner=method).scan()

        return output

    @logger.catch
    def show_output(self, output: Union[dict, None]) -> None:
        """
        Method to show the output
        :param output: dict: The output to show
        """
        # If there are errors
        if output is None:
            return

        # If there are no open ports
        if output['open_ports']['count'] == 0:
            mcwrite(LM.get(f'commands.{self.name}.noOpenPorts').replace('%ip%', output['target']))
            return

        add_servers: bool = Input(LM.get(f'commands.addServersFoundToMinecraft'), 'boolean').get_input()

        if add_servers is None:
            return

        if add_servers:
            add_vulnerable_servers_only: bool = Input(
                input_message=LM.get(f'commands.addBungeeExploitVulnerableServersOnly'),
                input_type='boolean'
            ).get_input()

            if add_vulnerable_servers_only is None:
                return

            if add_vulnerable_servers_only:
                ServersDAT().add_servers_dat_file(servers=output['open_ports']['bungeeExploitVulnerable'], vulnerable=True)

            else:
                ServersDAT().add_servers_dat_file(servers=output['open_ports']['minecraft'])

        mcwrite(LM.get(f'commands.{self.name}.openPorts').replace('%openPorts%', str(output['open_ports']['count'])))
