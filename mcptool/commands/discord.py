from loguru import logger

from ..banners.show_banner import ShowBanner
from ..constants.banners import DiscordBanners


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
        ShowBanner(DiscordBanners.DISCORD_BANNER_1).show()
        return True
