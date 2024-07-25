import sys

from mcptool.utilities.constants_utilities import ConstantsUtilities


class URLS:
    GITHUB_REPOSITORY: str = 'https://github.com/pedroagustinvega/development'
    RAW_GITHUB_REPOSITORY: str = 'https://raw.githubusercontent.com/pedroagustinvega/mcptool/development'
    MCPTOOL_VELOCITY_JAR_URL: str = 'https://github.com/pedroagustinvega/mcptool-velocity/releases/download/1.0.0/MCPTool-Velocity.jar'
    RFAKEPROXY_JAR_URL: str = 'https://github.com/pedroagustinvega/rfakeproxy/releases/download/1.0.0/RFakeProxy.jar'
    DISCORD_SERVER: str = 'discord.gg/TWKs6BWkR2'
    MCPTOOL_WEBSITE: str = 'mcptool.net'
    NORDIFY_DISCORD: str = 'https://discord.gg/ducks'


class Emojis:
    TIME_EMOJI: str = '⏰'
    ERROR_EMOJI: str = '❌'
    SUCCESS_EMOJI: str = '✅'
    INFO_EMOJI: str = 'ℹ️'
    WARNING_EMOJI: str = '⚠️'
    PREFIX_EMOJI: str = '🔰'
    PICKAXE_EMOJI: str = '⛏️'


class MCPToolStrings:
    VERSION: str = '1.0.7'
    PREFIX: str = f'&c&l«{Emojis.PREFIX_EMOJI}&c&l»&r'
    SPACES: str = ' ' * 4
    OS_NAME: str = ConstantsUtilities.get_os_name()
    BUUNGE_EXPLOIT_VULNERABLE_MESSAGE: str = '§cVulnerable to Bungee Exploit'


class CLI:
    value: bool = True if len(sys.argv) > 1 else False
