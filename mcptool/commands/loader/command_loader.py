from mcptool.commands.server import Command as ServerCommand
from mcptool.commands.uuid import Command as UUIDCommand
from mcptool.commands.ipinfo import Command as IPInfoCommand
from mcptool.commands.iphistory import Command as IPHistoryCommand
from mcptool.commands.dnslookup import Command as DNSLookupCommand
from mcptool.commands.checker import Command as CheckerCommand
from mcptool.commands.password import Command as PasswordCommand
from mcptool.commands.seeker import Command as SeekerCommand
from mcptool.commands.websearch import Command as WebSearchCommand
from mcptool.commands.subdomains import Command as SubdomainsCommand
from mcptool.commands.scan import Command as ScanCommand
from mcptool.commands.listening import Command as ListeningCommand
from mcptool.commands.proxy import Command as ProxyCommand
from mcptool.commands.fakeproxy import Command as FakeProxyCommand
from mcptool.commands.connect import Command as ConnectCommand
from mcptool.commands.sendcmd import Command as SendCMDCommand
from mcptool.commands.rcon import Command as RconCommand
from mcptool.commands.brutercon import Command as BruteRconCommand
from mcptool.commands.bruteauth import Command as BruteAuthCommand
from mcptool.commands.kick import Command as KickCommand
from mcptool.commands.kickall import Command as KickAllCommand
from mcptool.commands.clearservers import Command as ClearServersCommand


class CommandLoader:
    @staticmethod
    def load_commands() -> dict:
        """
        Load all commands
        :return: Dict with all commands loaded
        """
        commands: dict = {
            'server': ServerCommand(),
            'uuid': UUIDCommand(),
            'ipinfo': IPInfoCommand(),
            'iphistory': IPHistoryCommand(),
            'dnslookup': DNSLookupCommand(),
            'checker': CheckerCommand(),
            'password': PasswordCommand(),
            'seeker': SeekerCommand(),
            'websearch': WebSearchCommand(),
            'subdomains': SubdomainsCommand(),
            'scan': ScanCommand(),
            'listening': ListeningCommand(),
            'proxy': ProxyCommand(),
            'fakeproxy': FakeProxyCommand(),
            'connect': ConnectCommand(),
            'sendcmd': SendCMDCommand(),
            'rcon': RconCommand(),
            'brutercon': BruteRconCommand(),
            'bruteauth': BruteAuthCommand(),
            'kick': KickCommand(),
            'kickall': KickAllCommand(),
            'clearservers': ClearServersCommand(),
        }
        return commands
