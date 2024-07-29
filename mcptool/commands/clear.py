import random

from loguru import logger

from ..banners.show_banner import ShowBanner
from ..constants.banners import MCPToolBanners


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'clear'

    @logger.catch
    def execute(self, user_arguments: list = []) -> bool:
        """
        Method to execute the command
        :param user_arguments: The arguments to execute the command
        """
        banner: str = MCPToolBanners.BANNERS[random.randint(0, len(MCPToolBanners.BANNERS) - 1)]
        ShowBanner(banner, clear_screen=True).show()
        return True
