from loguru import logger
from mccolors import mcwrite

from mcptool.nbt.servers_dat import ServersDAT
from mcptool.utilities.language.utilities import LanguageUtils as LM


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'clearservers'
        self.command_arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]
        logger.debug(f"Command initialized: {self.name}, arguments: {self.command_arguments}")

    @logger.catch
    def execute(self, user_arguments: list) -> None:
        """
        Method to execute the command
        :param user_arguments: list: The arguments to execute the command
        """
        mcwrite(LM.get(f'commands.{self.name}.serversCleared'))
        ServersDAT().remove_servers_dat_file()
