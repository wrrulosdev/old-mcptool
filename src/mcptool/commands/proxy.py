from loguru import logger
from mccolors import mcwrite

from ..commands.arguments.argument_validator import ValidateArgument
from ..minecraft.proxy.start_proxy import StartProxy
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'proxy'
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

        if not ValidateArgument.is_domain(domain=user_arguments[0]) and not ValidateArgument.is_ip_and_port(
                ip=user_arguments[0]) and not ValidateArgument.is_domain_and_port(domain=user_arguments[0]):
            mcwrite(Lm.get('errors.invalidServerFormat'))
            return False

        if not ValidateArgument.is_velocity_forwading_mode(user_arguments[1]):
            mcwrite(Lm.get('errors.invalidVelocityMode'))
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
        server: str = user_arguments[0]
        forwarding_mode: str = user_arguments[1]

        # Execute the command
        StartProxy(server=server, forwarding_mode=forwarding_mode).start()
        return True
