import random
import shutil
import struct
import threading
import time
import os

import pypresence
from loguru import logger
from mccolors import mcwrite, mcreplace
from ezjsonpy import load_languages, set_language, load_configurations, get_config_value

from mcptool.constants import MCPToolStrings, URLS
from mcptool.path.mcptool_path import MCPToolPath
from mcptool.scrappers.minecraftservers import MinecraftServerScrapper
from mcptool.utilities.text.command_finished_message import CommandFinishedMessage

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
    {'name': 'nordify', 'path': os.path.join(mcptool_path.get_path(), 'settings', 'nordify.json')},
    {'name': 'scanner', 'path': os.path.join(mcptool_path.get_path(), 'settings', 'scanner.json')},
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
        self.active_command: str = 'In the main menu'
        self.mcptool_path: MCPToolPath = mcptool_path
        self.commands = CommandLoader.load_commands()
        self.minecraft_scrapper: MinecraftServerScrapper = MinecraftServerScrapper()
        self.commands_with_time_available: list = ['seeker', 'scan', 'bruteauth', 'brutercon', 'rcon', 'sendcmd']

    @logger.catch
    def run(self):
        logger.info(f'Starting MCPTool v{MCPToolStrings.VERSION}')
        ShowBanner(
            banner=LoadingBanners.LOADING_BANNER_1,
            clear_screen=True
        ).show()

        if get_config_value('discordPresence'):
            rich_presence_thread = threading.Thread(target=self._update_rich_presence, args=([]))
            rich_presence_thread.daemon = True
            rich_presence_thread.start()

        time.sleep(1.5)
        self._command_loop()

    @logger.catch
    def _command_loop(self):
        """Method to run the command loop"""
        banner: str = MCPToolBanners.BANNERS[random.randint(0, len(MCPToolBanners.BANNERS) - 1)]
        ShowBanner(banner, clear_screen=True).show()

        while True:
            try:
                arguments: list = input(mcreplace(InputBanners.INPUT_1)).split()
                start_time: float = time.time()

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
                    command_instance = self.commands[command]

                    if command == 'websearch':
                        output: bool = command_instance.execute(arguments[1:], scrapper=self.minecraft_scrapper)

                    else:
                        output: bool = command_instance.execute(arguments[1:])

                    if output:
                        self.active_command = f'Using the {command} command'

                        if command not in self.commands_with_time_available:
                            continue

                        stop_time: float = time.time()
                        command_time: float = stop_time - start_time
                        command_finished_message: str = CommandFinishedMessage(command_time=command_time).get_message()
                        mcwrite(command_finished_message)

                except KeyboardInterrupt:
                    mcwrite(Lm.get('commands.ctrlC'))

            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                break

    @logger.catch
    def _update_rich_presence(self) -> None:
        """Method to update the rich presence"""
        rpc: pypresence.Presence = pypresence.Presence(MCPToolStrings.MCPTOOL_DISCORD_CLIENT_ID)
        start_time: int = int(time.time())

        try:
            # Connect to the Discord client
            rpc.connect()
            logger.info('Connected to the Discord client')

            while True:
                rpc.update(
                    state=self.active_command,
                    details=f'Pentesting Tool for Minecraft (v{MCPToolStrings.VERSION})',
                    start=start_time,
                    large_image='logo',
                    large_text='Pentesting Tool for Minecraft',
                    small_image='small_logo',
                    small_text=f'Version: {MCPToolStrings.VERSION}',
                    buttons=[
                        {'label': 'Website', 'url': URLS.MCPTOOL_WEBSITE},
                        {'label': 'Discord', 'url': URLS.DISCORD_SERVER}
                    ]
                )

                time.sleep(1)

        except (pypresence.exceptions.DiscordNotFound, struct.error, pypresence.exceptions.ServerError,
                pypresence.exceptions.ResponseTimeout) as e:
            logger.error(f'Failed to connect to the Discord client. Error: {e}. Retrying in 30 seconds...')
            time.sleep(30)
            self._update_rich_presence()

        except (KeyboardInterrupt, ValueError, RuntimeError, OSError):
            logger.error('Failed to connect to the Discord client. Retrying in 30 seconds...')
            pass

    @logger.catch
    def _remove_python_files(self) -> None:
        """Remove the python files in the AppData directory after the update"""
        appdata_path: str = os.getenv('APPDATA')  # %appdata%
        lib_folder_path: str = os.path.abspath(os.path.join(appdata_path, 'lib'))  # %appdata%/lib

        if os.path.exists(lib_folder_path):
            shutil.rmtree(lib_folder_path)

        for file in os.listdir(appdata_path):
            if file == 'MCPToolUpdater.exe' or file == 'MCPTool-win64.msi':
                os.remove(os.path.join(appdata_path, file))

            if file.endswith('.dll'):
                if 'python' in file:
                    os.remove(os.path.join(os.getenv('APPDATA'), file))
