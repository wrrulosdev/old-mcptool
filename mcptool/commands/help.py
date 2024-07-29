import random

from loguru import logger

from ..banners.show_banner import ShowBanner
from ..constants.banners import HelpBanners


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'help'

    @logger.catch
    def execute(self, user_arguments: list = []) -> bool:
        """
        Method to execute the command
        :param user_arguments: The arguments to execute the command
        :return: bool: True if the command was executed successfully, False otherwise
        """
        banner: str = HelpBanners.BANNERS[random.randint(0, len(HelpBanners.BANNERS) - 1)]
        ShowBanner(banner).show()
        return True
