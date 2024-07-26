import random

from loguru import logger

from mcptool.banners.show_banner import ShowBanner
from mcptool.constants.banners import HelpBanners


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'help'

    @logger.catch
    def execute(self, user_arguments: list = []) -> bool:
        """
        Method to execute the command
        :param user_arguments: The arguments to execute the command
        """
        banner: str = HelpBanners.BANNERS[random.randint(0, len(HelpBanners.BANNERS) - 1)]
        ShowBanner(banner).show()
        return True
