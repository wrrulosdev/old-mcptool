from loguru import logger
from mccolors import mcwrite
from ezjsonpy import get_config_value, set_config_value


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'debug'

    @logger.catch
    def execute(self, user_arguments: list = []) -> bool:
        """
        Method to execute the command
        :param user_arguments: The arguments to execute the command
        :return: bool: True if the command was executed successfully, False otherwise
        """
        debug_value: bool = get_config_value('debug')

        if debug_value:
            mcwrite(f'commands.debug.disabled')
            set_config_value('debug', False)
            logger.info('Debug mode disabled')

        else:
            mcwrite(f'commands.debug.enabled')
            set_config_value('debug', True)
            logger.info('Debug mode enabled')

        return True