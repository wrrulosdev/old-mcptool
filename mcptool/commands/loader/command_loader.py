from ...commands.bruteauth import Command as BruteAuthCommand
from ...commands.brutercon import Command as BruteRconCommand
from ...commands.checker import Command as CheckerCommand
from ...commands.clear import Command as ClearCommand
from ...commands.clearservers import Command as ClearServersCommand
from ...commands.connect import Command as ConnectCommand
from ...commands.discord import Command as DiscordCommand
from ...commands.dnslookup import Command as DNSLookupCommand
from ...commands.fakeproxy import Command as FakeProxyCommand
from ...commands.help import Command as HelpCommand
from ...commands.iphistory import Command as IPHistoryCommand
from ...commands.ipinfo import Command as IPInfoCommand
from ...commands.kick import Command as KickCommand
from ...commands.kickall import Command as KickAllCommand
from ...commands.listening import Command as ListeningCommand
from ...commands.password import Command as PasswordCommand
from ...commands.proxy import Command as ProxyCommand
from ...commands.rcon import Command as RconCommand
from ...commands.resolver import Command as ResolverCommand
from ...commands.scan import Command as ScanCommand
from ...commands.seeker import Command as SeekerCommand
from ...commands.sendcmd import Command as SendCMDCommand
from ...commands.server import Command as ServerCommand
from ...commands.settings import Command as SettingsCommand
from ...commands.subdomains import Command as SubdomainsCommand
from ...commands.uuid import Command as UUIDCommand
from ...commands.websearch import Command as WebSearchCommand
from ...commands.debug import Command as DebugCommand


class CommandLoader:
    @staticmethod
    def load_commands() -> dict:
        """
        Load all commands
        :return: Dict with all commands loaded
        """
        commands: dict = {
            'help': HelpCommand(),
            'clear': ClearCommand(),
            'server': ServerCommand(),
            'uuid': UUIDCommand(),
            'ipinfo': IPInfoCommand(),
            'iphistory': IPHistoryCommand(),
            'dnslookup': DNSLookupCommand(),
            'checker': CheckerCommand(),
            'resolver': ResolverCommand(),
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
            'settings': SettingsCommand(),
            'discord': DiscordCommand(),
            'debug': DebugCommand()
        }
        return commands
