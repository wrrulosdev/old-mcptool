import time
import os

from loguru import logger
from mccolors import mcwrite
from ezjsonpy import load_languages, set_language, load_configuration, get_config_value

from mcptool.path.mcptool_path import MCPToolPath
from mcptool.commands.loader.command_loader import CommandLoader


class MCPTool:
    def __init__(self):
        self.commands: dict = {}
        self.active_command: str = ''
        self.version: str = '1.0.7'
        self.mcptool_path: MCPToolPath = MCPToolPath()
        self.commands = CommandLoader.load_commands()

    @logger.catch
    def run(self):
        logger.info(f'Starting MCPTool v{self.version}')
        # Load the settings and languages
        self._load_settings()
        self._load_languages()
        set_language(get_config_value('language'))
        # Run the command loop
        self._command_loop()

    @logger.catch
    def _load_settings(self):
        """Method to load the settings"""
        load_configuration(
            'default',
            os.path.join(self.mcptool_path.get_path(), 'settings.json')
        )

    @logger.catch
    def _load_languages(self):
        """Method to load the languages"""
        load_languages([
            {'name': 'en', 'path': os.path.join(self.mcptool_path.get_path(), 'languages', 'en.json')}
        ])

    @logger.catch
    def _command_loop(self):
        """Method to run the command loop"""

        while True:
            try:
                arguments: list = input('mcptool ~ ').split()

                if len(arguments) == 0:
                    continue

                command: str = arguments[0].lower()

                if command == 'exit':
                    break

                if command not in self.commands:
                    continue

                try:
                    # Start the command timer
                    start_time: float = time.time()

                    command_instance = self.commands[command]
                    command_instance.execute(arguments[1:])

                except KeyboardInterrupt:
                    mcwrite('Command interrupted')

            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                break
