from typing import Union

from loguru import logger
from mccolors import mcwrite, mcreplace
from mcrcon import MCRcon, MCRconException

from ..commands.arguments.argument_validator import ValidateArgument
from ..constants import MCPToolStrings, CLI
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'rcon'
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
        rcon_password: str = user_arguments[1]
        mcr: Union[MCRcon, None] = None

        mcwrite(Lm.get(f'commands.{self.name}.connecting')
                .replace('%ip%', f'{ip_address}:{port}')
                )

        try:
            with MCRcon(host=ip_address, password=rcon_password, port=int(port), timeout=30) as mcr:
                mcwrite(Lm.get(f'commands.{self.name}.connected'))

                while True:
                    command: str = input(mcreplace(Lm.get(f'commands.{self.name}.commandInput')))

                    if command == '.exit':
                        mcwrite(Lm.get(f'commands.{self.name}.disconnected'))
                        mcr.disconnect()
                        break

                    response: str = mcr.command(command)
                    spaces: str = '0' if CLI.value else MCPToolStrings.SPACES
                    mcwrite(f'{spaces}{response}')

        except TimeoutError:
            mcwrite(Lm.get('errors.rconTimeout'))

        except ConnectionRefusedError:
            mcwrite(Lm.get('errors.rconConnectionRefused'))

        except MCRconException:
            mcwrite(Lm.get('errors.rconInvalidPassword'))

        except KeyboardInterrupt:
            if mcr:
                mcr.disconnect()

            mcwrite(Lm.get(f'commands.{self.name}.disconnected'))

        except Exception as e:
            mcwrite(Lm.get('errors.rconUnknownError'))
            logger.error(f'Error in rcon command: {e}')

        return True
