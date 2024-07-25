"""
mcptool.__main__

This module contains the main entry point for running the MCPTool.
"""

import sys

from mccolors import mcwrite
from mcptool import MCPTool

from mcptool.constants import MCPToolStrings


def main():
    """
    Main function to run the MCPTool
    """

    help_message: str = """
&f&lUsage: &a&lmcptool [command]

&f&lCommands:

&f&l  help &8- &f&lShow the help message
&f&l  version &8- &f&lShow the version of the tool
"""
    mcptool_obj: MCPTool = MCPTool()

    if len(sys.argv) == 1:
        mcptool_obj.run()
        return

    # Run mcptool in command line mode
    command: str = sys.argv[1].lower()

    if command == 'help':
        mcwrite(help_message)
        return

    if command == 'version':
        print(MCPToolStrings.VERSION)
        return

    if command not in mcptool_obj.commands:
        mcwrite(help_message)
        return

    arguments: list = sys.argv[2:]
    command_instance = mcptool_obj.commands.get(command)
    command_instance.execute(arguments)
