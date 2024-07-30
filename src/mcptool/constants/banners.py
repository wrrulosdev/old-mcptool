from . import MCPToolStrings, URLS
from .update_available import UPDATE_AVAILABLE
from ..utilities.language.utilities import LanguageUtils as Lm


class LoadingBanners:
    LOADING_BANNER_1: str = f'''
\n\n\n\n\n
                                                ⠀⠀⠀⠀⠀⠀⠀⠀&b⢀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
                                                ⠀⠀⠀⠀⠀⠀&b⢀⣀⡿⠿⠿⠿⠿⠿⠿⢿⣀⣀⣀&f&l⣀⣀⡀⠀⠀
                                                ⠀⠀⠀⠀⠀⠀&b⠸⠿⣇⣀⣀⣀⣀⣀⣀⣸⠿⢿⣿&f&l⣿⣿⡇⠀⠀          
                                                ⠀⠀⠀⠀⠀⠀⠀⠀&b⠻⠿⠿⠿⠿⠿⣿⣿⣀⡸⠿⢿⣿⡇⠀⠀
                                                ⠀⠀⠀⠀⠀⠀⠀⠀&f&l⠀⠀⠀⠀⣤⣤⣿⣿⣿&b⣧⣤⡼⠿⢧⣤⡀         
                                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀&f&l⣤⣤⣿⣿⣿⣿⠛&b⢻⣿⡇⠀⢸⣿⡇
                                                ⠀⠀⠀⠀⠀⠀⠀⠀&f&l⣤⣤⣿⣿⣿⣿⠛⠛⠀&b⢸⣿⡇⠀⢸⣿⡇          
                                                ⠀⠀⠀⠀⠀⠀&f&l⢠⣤⣿⣿⣿⣿⠛⠛⠀⠀⠀&b⢸⣿⡇⠀⢸⣿⡇
                                                ⠀⠀⠀⠀&f&l⢰⣶⣾⣿⣿⣿⠛⠛⠀⠀⠀⠀⠀&b⠈⠛⢳⣶⡞⠛⠁   
                                                ⠀⠀&f&l⢰⣶⣾⣿⣿⣿⡏⠉⠀⠀⠀⠀⠀⠀⠀&b⠀⠀⠈⠉⠁⠀⠀
                                                &f&l⢰⣶⡎⠉⢹⣿⡏⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                                &f&l⢸⣿⣷⣶⡎⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                                ⠀&f&l⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀'''


class MCPToolBanners:
    BANNER_1: str = f'''
&f&l        dMMMMMMMMb  .aMMMb  dMMMMb&c&l dMMMMMMP .aMMMb  .aMMMb  dMP
&f&l       dMP"dMP"dMP dMP"VMP dMP.dMP&c&l   dMP   dMP"dMP dMP"dMP dMP
&f&l      dMP dMP dMP dMP     dMMMMP"&c&l   dMP   dMP dMP dMP dMP dMP
&f&l     dMP dMP dMP dMP.aMP dMP&c&l       dMP   dMP.aMP dMP.aMP dMP
&f&l    dMP dMP dMP  VMMMP" dMP&c&l       dMP    VMMMP"  VMMMP" dMMMMMP

{Lm.get('app.description').replace('%version%', MCPToolStrings.VERSION)}{Lm.get('app.newVersion') if UPDATE_AVAILABLE else ''}'''

    BANNER_2: str = f'''
&f&l    ███╗   ███╗ ██████╗██████╗ &c&l████████╗ ██████╗  ██████╗ ██╗
&f&l    ████╗ ████║██╔════╝██╔══██╗&c&l╚══██╔══╝██╔═══██╗██╔═══██╗██║
&f&l    ██╔████╔██║██║     ██████╔╝&c&l   ██║   ██║   ██║██║   ██║██║
&f&l    ██║╚██╔╝██║██║     ██╔═══╝ &c&l   ██║   ██║   ██║██║   ██║██║
&f&l    ██║ ╚═╝ ██║╚██████╗██║     &c&l   ██║   ╚██████╔╝╚██████╔╝███████╗
&f&l    ╚═╝     ╚═╝ ╚═════╝╚═╝     &c&l   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

{Lm.get('app.description').replace('%version%', MCPToolStrings.VERSION)}{Lm.get('app.newVersion') if UPDATE_AVAILABLE else ''}'''

    BANNER_3: str = f'''
&f&l    8888ba.88ba   a88888b.  888888ba  &c&ld888888P                   dP
&f&l    88  `8b  `8b d8'   `88  88    `8b &c&l   88                      88
&f&l    88   88   88 88        a88aaaa8P' &c&l   88    .d8888b. .d8888b. 88
&f&l    88   88   88 88         88        &c&l   88    88'  `88 88'  `88 88
&f&l    88   88   88 Y8.   .88  88        &c&l   88    88.  .88 88.  .88 88
&f&l    dP   dP   dP  Y88888P'  dP        &c&l   dP    `88888P' `88888P' dP

{Lm.get('app.description').replace('%version%', MCPToolStrings.VERSION)}{Lm.get('app.newVersion') if UPDATE_AVAILABLE else ''}'''

    BANNER_4: str = f'''
&f&l    `7MMM.     ,MMF' .g8"""bgd `7MM"""Mq. &c&lMMP""MM""YMM              `7MM
&f&l      MMMb    dPMM .dP'     `M   MM   `MM.&c&lP'   MM   `7                MM
&f&l      M YM   ,M MM dM'       `   MM   ,M9 &c&l     MM  ,pW"Wq.   ,pW"Wq.  MM
&f&l      M  Mb  M' MM MM            MMmmdM9  &c&l     MM 6W'   `Wb 6W'   `Wb MM
&f&l      M  YM.P'  MM MM.           MM       &c&l     MM 8M     M8 8M     M8 MM
&f&l      M  `YM'   MM `Mb.     ,'   MM       &c&l     MM YA.   ,A9 YA.   ,A9 MM
&f&l    .JML. `'  .JMML. `"bmmmd'  .JMML.     &c&l   .JMML.`Ybmd9'   `Ybmd9'.JMML.

{Lm.get('app.description').replace('%version%', MCPToolStrings.VERSION)}{Lm.get('app.newVersion') if UPDATE_AVAILABLE else ''}'''

    BANNERS: list = [BANNER_1, BANNER_2, BANNER_3, BANNER_4]


class InputBanners:
    INPUT_1 = f'\n{MCPToolStrings.SPACES}&8&l{MCPToolStrings.OS_NAME}@mcptool ~\n{MCPToolStrings.SPACES} &c&l↪ &f&l'


class HelpBanners:
    HELP_BANNER_1 = f'''                                                                             &d      ⣠⠤⠖⠚⢉⣩⣭⡭⠛⠓⠲⠦⣄⡀
    &c• &f&lCommands:                                                          &d       ⢀⡴⠋⠁  ⠊         ⠉⠳⢦⡀
                                                                         &d     ⢀⡴⠃⢀⡴⢳               ⠙⣆
      &d► &f&lserver [ip:port/domain]                                          &d     ⡾⠁⣠⠋ ⠈⢧               ⠈⢧
      &d► &f&luuid [username/UUID]                                             &d    ⣸⠁⢰⠃   ⠈⢣⡀              ⠈⣇
      &d► &f&lipinfo [ip]                                                      &d    ⡇ ⡾⡀    ⣀⣹⣆⡀             ⢹
      &d► &f&liphistory [domain]                                               &d   ⢸⠃⢀⣇⡈      &d⢀⡑⢄⡀⢀⡀         ⢸⡇
      &d► &f&ldnslookup [domain]                                               &d   ⢸ &f&l⢻⡟⡻⢶⡆   ⡼⠟⡳⢿⣦&d⡑⢄         ⢸⡇
      &d► &f&lchecker [file]                                                   &d   ⣸ &f&l⢸⠃⡇⢀⠇     ⡼  ⠈⣿&d⡗⠂       ⢸⠁
      &d► &f&lresolver [domain]                                                &d   ⡏ &f&l⣼ ⢳⠊      ⠱⣀⣀⠔&d⣸⠁       ⢠⡟
      &d► &f&lseeker [token/servers]                                           &d   ⡇&f&l⢀⡇           ⠠ &d⡇        ⢸⠃
      &d► &f&lwebsearch                                                        &d  ⢸⠃&f&l⠘⡇            &d⢸⠁  ⢀     ⣾
      &d► &f&lsubdomains [domain] [wordlist]                                   &d  ⣸  &f&l⠹⡄  ⠈⠁       &d⡞   ⠸     ⡇
      &d► &f&lscan [ip_address/ip_range] [port/port_range] [method]            &d  ⡏   &f&l⠙⣆       ⢀⣠⢶&d⡇  ⢰⡀     ⡇
      &d► &f&llistening [ip:port/domain]                                       &d ⢰⠇⡄    &f&l⢣⣀⣀⣀⡤⠴⡞⠉ &d⢸   ⣿⡇     ⣧
      &d► &f&lproxy [ip:port/domain] [velocity_forwading_mode]                 &d ⣸ ⡇       &f&l   ⢹  &d⢸  ⢀⣿⠇   ⠁ ⢸
      &d► &f&lfakeproxy [ip:port/domain] [velocity_forwading_mode]             &d ⣿ ⡇    &f&l ⢀⡤⠤⠶⠶⠾⠤⠄&d⢸ ⡀⠸⣿⣀     ⠈⣇
      &d► &f&lconnect [ip:port/domain] [version] [username]                    &d ⡇ ⡇    &f&l⡴⠋       &d⠸⡌⣵⡀⢳⡇      ⢹⡀
      &d► &f&lsendcmd [ip:port/domain] [version] [username] [commands_file]    &d ⡇ ⠇   &f&l⡸⠁         &d⠙⠮⢧⣀⣻⢂      ⢧
      &d► &f&lrcon [ip:port] [password]                                        &d ⣇ ⢠   &f&l⠇            &d  ⠈⡎⣆     ⠘
      &d► &f&lbrutercon [ip:port] [passwords_file]                             &d ⢻ ⠈⠰ &f&l⢸             &d  ⠰⠘⢮⣧⡀
      &d► &f&lbruteauth [ip:port/domain] [version] [username] [passwords_file] &d ⠸⡆  ⠇&f&l⣾             &d     ⠙⠳⣄⡀⡀
      &d► &f&lkick [ip:port/domain] [version] [username] [loop]                &d ⠸⡆  ⠇&f&l⣾             &d         ⠙⡀⢢
      &d► &f&lkickall [ip:port/domain] [version] [loop]                        &d ⠸⡆  ⠇&f&l⣾             &d          ⠙⡀⢢
      &d► &f&lpassword [username/s]                                            &d  ⡏   &f&l⠙⣆       ⢀⣠⢶⡇  ⢰⡀     ⡇
      
    &b• &f&lOther commands: &f&ldiscord settings clearservers debug clear'''

    CLI_BANNER: str = f'''
&f&lUsage: &a&lmcptool [command]

&f&lCommands:

  &b&lhelp &8- &f&lShow the help message
  &b&lversion &8- &f&lShow the version of the tool
  &b&lserver &8- &f&lCheck the status of a Minecraft server
  &b&luuid &8- &f&lGet the UUID of a Minecraft player
  &b&lipinfo &8- &f&lGet information about an IP address
  &b&liphistory &8- &f&lGet the history of an IP address
  &b&ldnslookup &8- &f&lLookup the DNS of a domain
  &b&lchecker &8- &f&lCheck the status of a list of servers in a text file
  &b&lresolver &8- &f&lResolve a domain to an IP address
  &b&lseeker &8- &f&lGet minecraft servers using the seeker api
  &b&lwebsearch &8- &f&lGet minecraft servers from the multiple websites
  &b&lsubdomains &8- &f&lGet the subdomains of a domain using a wordlist
  &b&lscan &8- &f&lScan a Minecraft server or a range of IP addresses
  &b&llistening &8- &f&lGet the players of a Minecraft server
  &b&lproxy &8- &f&lStart a proxy server using Velocity
  &b&lfakeproxy &8- &f&lStart a fake proxy server with RFakeProxy plugin
  &b&lconnect &8- &f&lConnect to a Minecraft server using Mineflayer
  &b&lsendcmd &8- &f&lSend mineflayer bot to a Minecraft server and execute commands from a file
  &b&lrcon &8- &f&lConnect to a Minecraft server using RCON
  &b&lbrutercon &8- &f&lBrute force the RCON password of a Minecraft server
  &b&lbruteauth &8- &f&lBrute force the authentication of a Minecraft server
  &b&lkick &8- &f&lKick a player from a Minecraft server
  &b&lkickall &8- &f&lKick all players from a Minecraft server
  &b&lpassword &8- &f&lGet the password of a Minecraft player using the Nordify API
  &b&ldiscord &8- &f&lOpen the discord server
  &b&lsettings &8- &f&lChange the settings of the tool
  &b&lclearservers &8- &f&lClear the minecraft server list (servers.dat)
  &b&lclear &8- &f&lClear the console'''

    BANNERS: list = [HELP_BANNER_1]


class DiscordBanners:
    DISCORD_BANNER_1 = f'''
    &b                       &f&l• &5wRRulos Server
    &b                       &b&l{URLS.DISCORD_SERVER}
    &b       ⢠⣴⣾⣵⣶⣶⣾⣿⣦⡄
    &b      ⢀⣾⣿⣿⢿⣿⣿⣿⣿⣿⣿⡄        &f&l- Enter my discord server
    &b      ⢸⣿⣿⣧⣀⣼⣿⣄⣠⣿⣿⣿        &f&l- to stay up to date with my projects
    &b      ⠘⠻⢷⡯⠛⠛⠛⠛⢫⣿⠟⠛        &f&l- and you can also talk to me!
    &b
    &b                       &c➥ &f&lWeb: &b{URLS.MCPTOOL_WEBSITE}'''
