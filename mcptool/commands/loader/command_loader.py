from mcptool.commands.server import Command as ServerCommand
from mcptool.commands.uuid import Command as UUIDCommand
from mcptool.commands.ipinfo import Command as IPInfoCommand
from mcptool.commands.fakeproxy import Command as FakeProxyCommand


class CommandLoader:
    @staticmethod
    def load_commands() -> dict:
        commands: dict = {
            'server': ServerCommand(),
            'uuid': UUIDCommand(),
            'ipinfo': IPInfoCommand(),
            'fakeproxy': FakeProxyCommand()
        }
        return commands
