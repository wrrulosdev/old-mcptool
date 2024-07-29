from plyer import notification

from .. import MCPToolPath
from ..utilities.termux.utilities import TermuxUtilities


class SendNotification:
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message

    def send(self) -> None:
        """Send a notification to the user with the title and message"""
        if TermuxUtilities.is_termux():
            return

        notification.notify(
            title=self.title,
            message=self.message,
            app_name='MCPTool',
            app_icon=f'{MCPToolPath.get_path()}/img/icon.ico',
            timeout=1
        )
