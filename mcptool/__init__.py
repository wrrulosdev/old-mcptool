import random
import time
import os

from loguru import logger
from mccolors import mcwrite, mcreplace
from ezjsonpy import load_languages, set_language, load_configurations, get_config_value
from mcptool.path.mcptool_path import MCPToolPath
from mcptool.scrappers.minecraftservers import MinecraftServerScrapper

# Remove the default logger
logger.remove()

# Set the logging configuration
logger.add(os.path.join(MCPToolPath.get_path(), 'logs.log'),
           level='INFO',
           format='[{time} {level} - {file}, {line}] ⮞ <level>{message}</level>',
           rotation="30 MB"
           )

mcptool_path: MCPToolPath = MCPToolPath()

load_languages([
    {'name': 'en', 'path': os.path.join(mcptool_path.get_path(), 'languages', 'en.json')}
])

load_configurations([
    {'name': 'default', 'path': os.path.join(mcptool_path.get_path(), 'settings', 'settings.json')},
    {'name': 'proxy', 'path': os.path.join(mcptool_path.get_path(), 'settings', 'proxy.json')}
])
set_language(get_config_value('language'))

from mcptool.commands.loader.command_loader import CommandLoader
from mcptool.banners.show_banner import ShowBanner
from mcptool.constants.banners import MCPToolBanners, LoadingBanners, InputBanners
from mcptool.utilities.language.utilities import LanguageUtils as Lm


class MCPTool:
    def __init__(self):
        self.commands: dict = {}
        self.active_command: str = ''
        self.version: str = '1.0.7'
        self.mcptool_path: MCPToolPath = mcptool_path
        self.commands = CommandLoader.load_commands()
        self.minecraft_scrapper: MinecraftServerScrapper = MinecraftServerScrapper()

    @logger.catch
    def run(self):
        logger.info(f'Starting MCPTool v{self.version}')
        # Show the loading banner
        ShowBanner(
            banner=LoadingBanners.LOADING_BANNER_1,
            clear_screen=True
        ).show()
        time.sleep(0.5)
        # Run the command loop
        self._command_loop()

    @logger.catch
    def _command_loop(self):
        """Method to run the command loop"""
        banner: str = MCPToolBanners.BANNERS[random.randint(0, len(MCPToolBanners.BANNERS) - 1)]
        ShowBanner(banner, clear_screen=True).show()

        while True:
            try:
                arguments: list = input(mcreplace(InputBanners.INPUT_1)).split()

                if len(arguments) == 0:
                    continue

                command: str = arguments[0].lower()

                if command == 'exit':
                    break

                if command not in self.commands:
                    mcwrite(Lm.get('commands.invalidCommand'))
                    continue

                try:
                    # Start the command timer
                    start_time: float = time.time()
                    command_instance = self.commands[command]

                    if command == 'websearch':
                        command_instance.execute(arguments[1:], scrapper=self.minecraft_scrapper)

                    else:
                        command_instance.execute(arguments[1:])

                except KeyboardInterrupt:
                    mcwrite(Lm.get('commands.ctrlC'))

            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                break
