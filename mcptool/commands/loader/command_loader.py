from mcptool.commands.server import Command as ServerCommand
from mcptool.commands.uuid import Command as UUIDCommand
from mcptool.commands.ipinfo import Command as IPInfoCommand
from mcptool.commands.iphistory import Command as IPHistoryCommand
from mcptool.commands.dnslookup import Command as DNSLookupCommand
from mcptool.commands.checker import Command as CheckerCommand
from mcptool.commands.password import Command as PasswordCommand
from mcptool.commands.seeker import Command as SeekerCommand
from mcptool.commands.proxy import Command as ProxyCommand
from mcptool.commands.fakeproxy import Command as FakeProxyCommand


class CommandLoader:
    @staticmethod
    def load_commands() -> dict:
        commands: dict = {
            'server': ServerCommand(),
            'uuid': UUIDCommand(),
            'ipinfo': IPInfoCommand(),
            'iphistory': IPHistoryCommand(),
            'dnslookup': DNSLookupCommand(),
            'checker': CheckerCommand(),
            'password': PasswordCommand(),
            'seeker': SeekerCommand(),
            'proxy': ProxyCommand(),
            'fakeproxy': FakeProxyCommand()
        }
        return commands
