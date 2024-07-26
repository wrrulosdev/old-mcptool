"""
mcptool.__main__

This module contains the main entry point for running the MCPTool.
"""

import sys

from mccolors import mcwrite
from mcptool import MCPTool

from mcptool.constants import MCPToolStrings, URLS
from mcptool.constants.banners import HelpBanners


def main():
    """
    Main function to run the MCPTool
    """

    mcptool_obj: MCPTool = MCPTool()

    if len(sys.argv) == 1:
        mcptool_obj.run()
        return

    # Run mcptool in command line mode
    command: str = sys.argv[1].lower()

    if command == 'help':
        mcwrite(HelpBanners.CLI_BANNER)
        return

    if command == 'version':
        print(MCPToolStrings.VERSION)
        return

    if command == 'discord':
        print(URLS.DISCORD_SERVER)
        return

    if command not in mcptool_obj.commands:
        mcwrite(HelpBanners.CLI_BANNER)
        return

    arguments: list = sys.argv[2:]
    command_instance = mcptool_obj.commands.get(command)
    command_instance.execute(arguments)
