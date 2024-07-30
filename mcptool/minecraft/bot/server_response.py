import subprocess
from subprocess import CompletedProcess

from ezjsonpy import get_config_value
from loguru import logger

from ...constants import MCPToolStrings
from ...path.mcptool_path import MCPToolPath
from ...utilities.minecraft.bot.utilities import BotUtilities
from ...utilities.text.utilities import TextUtilities


class BotServerResponse:
    def __init__(self, ip_address: str, port: int, version: str,
                 username: str = BotUtilities.get_bot_username()) -> None:
        self.ip_address = ip_address
        self.port = port
        self.version = version
        self.username = username
        self._response = None

    @logger.catch
    def get_response(self) -> str:
        """Get the response from the server"""
        # Send the command
        self._send_command()

        # Get the text from the json if it is a json
        self._response = TextUtilities.get_text_from_json(self._response)

        # Remove new lines and quotes and return the response
        self._response = self._response.replace('\n', '').replace('"', '').replace("'", '')
        return self._response

    @logger.catch
    def _send_command(self) -> None:
        """Send the command to the server"""
        if get_config_value('debug'):
            logger.debug(f'Sending command: {self._get_command()}')

        response: CompletedProcess = subprocess.run(self._get_command(), shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)

        # Check if there is an error
        if response.stderr:
            error_message = response.stderr.decode('utf-8')

            if '^C' in error_message:
                self._response = '&cCtrl+C was pressed, the command was not sent to the server'
                return

            if '"node"' in error_message:
                self._response = '&cNode.js is not installed on the system'
                return

            if 'Error [ERR_MODULE_NOT_FOUND]: Cannot find package' in error_message:
                self._response = '&cNode.js modules are missing'
                return

            logger.warning(f'Error sending command: {self._get_command()} -> {error_message}')
            self._response = '&cError (Check the logs)'
            return

        self._response: str = response.stdout.decode('utf-8')

    @logger.catch
    def _get_command(self) -> str:
        """
        Method to get the command to send to the server
        :return: The command to send to the server
        """
        path: str = MCPToolPath.get_path()
        command: str = f'cd {path} && node scripts/server_response.mjs {self.ip_address} {self.port} {self.username} {self.version}'

        if MCPToolStrings.OS_NAME == 'windows':
            command = f'C: && {command}'

        return command
