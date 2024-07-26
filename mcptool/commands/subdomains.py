import os
import socket
import threading
import time

from ezjsonpy import get_config_value
from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'subdomains'
        self.command_arguments: list = [i for i in Lm.get(f'commands.{self.name}.arguments')]
        self.subdomain_found_message: str = Lm.get(f'commands.{self.name}.subdomainFound')
        self.subdomains_found: int = 0
        self.first_subdomain_found: bool = False
        self.stopped: bool = False
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

        if not os.path.exists(user_arguments[1]):
            mcwrite(Lm.get('errors.invalidFile'))
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
        file_path: str = user_arguments[1]

        # Execute the command
        try:
            num_threads: int = int(get_config_value('subdomainsThreads'))

        except ValueError:
            logger.warning(f'Invalid value for subdomainsThreads. Using default value (500)')
            num_threads: int = 500

        with open(file_path, 'r') as file:
            subdomain_list = [line.strip() for line in file]

        if len(subdomain_list) == 0:
            mcwrite(Lm.get('errors.subdomainsFileEmpty'))
            return False

        mcwrite(Lm.get(f'commands.{self.name}.wordlist')
                .replace('%file%', file_path)
                .replace('%subdomains%', str(len(subdomain_list)))
                )
        time.sleep(0.5)
        mcwrite(Lm.get(f'commands.{self.name}.gettingSubdomains'))

        # Check if the number of threads is greater than the number of subdomains
        if len(subdomain_list) < num_threads:
            num_threads = len(subdomain_list)

        # Divide the subdomains into chunks
        chunk_size = len(subdomain_list) // num_threads
        chunks = [subdomain_list[i:i + chunk_size] for i in range(0, len(subdomain_list), chunk_size)]

        # Create the threads
        threads: list = []

        try:
            # Scan the subdomains
            for chunk in chunks:
                thread = threading.Thread(target=self._scan_chunk, args=(domain, chunk))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finishes
            for thread in threads:
                thread.join()

            if self.subdomains_found == 0:
                mcwrite(Lm.get(f'commands.{self.name}.noSubdomains')
                        .replace('%file%', file_path)
                        )

            else:
                mcwrite(Lm.get(f'commands.{self.name}.subdomainsFound')
                        .replace('%subdomains%', str(self.subdomains_found))
                        )

        except KeyboardInterrupt:
            # Kill all threads
            self.stopped = True

        return True

    @logger.catch
    def _scan_subdomain(self, domain: str, subdomain: str) -> None:
        """
        Method to scan a subdomain.
        :param domain: str: The domain
        :param subdomain: str: The subdomain
        """
        try:
            host: str = f'{subdomain}.{domain}'
            ip: str = socket.gethostbyname(host)

            if not self.first_subdomain_found:
                print('')
                self.first_subdomain_found = True

            mcwrite(self.subdomain_found_message
                    .replace('%subdomain%', f'{subdomain}.{domain}')
                    .replace('%ip%', ip)
                    )
            self.subdomains_found += 1

        except (socket.gaierror, UnicodeError):
            return

    @logger.catch
    def _scan_chunk(self, domain: str, chunk: list) -> None:
        """
        Method to scan a chunk of subdomains
        :param domain: str: The domain
        :param chunk: list: The chunk of subdomains
        """
        for subdomain in chunk:
            if self.stopped:
                break

            self._scan_subdomain(domain, subdomain)
