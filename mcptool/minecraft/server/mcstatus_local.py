import socket
from typing import Union

from loguru import logger
from mcstatus import JavaServer, BedrockServer
from mcstatus.status_response import JavaStatusResponse, BedrockStatusResponse

from . import JavaServerData, BedrockServerData, clean_output
from ..bot.server_response import BotServerResponse
from ...utilities.minecraft.bot.utilities import BotUtilities
from ...utilities.minecraft.get_ip_port import GetMCIPPort


class MCServerData:
    def __init__(self, server: str, bot: bool) -> None:
        self.server = server
        self.bot = bot
        self.ip_address: Union[str, None] = None
        self.port: Union[int, None] = None

    @logger.catch
    def get(self) -> Union[JavaServerData, BedrockServerData, None]:
        """
        Method to get the server data from the server.
        :return: The server data if the server is online, otherwise None
        """
        output: Union[tuple[str, int], None] = GetMCIPPort(server=self.server).get_ip_port()

        if output is None:
            return None

        self.ip_address, self.port = output
        data: Union[JavaServerData, BedrockServerData, None] = self.get_server_data(
            function=JavaServer(self.ip_address, self.port))

        if data is None:
            self.port = 19132
            data: Union[JavaServerData, BedrockServerData, None] = self.get_server_data(
                function=BedrockServer(self.ip_address, self.port))

        return data

    @logger.catch
    def get_server_data(self, function: Union[JavaServer, BedrockServer]) -> Union[
        JavaServerData, BedrockServerData, None]:
        """
        Method to get the server data from the server.
        :param function: The server function.
        :return: The server data if the server is online, otherwise None
        """
        try:
            data: Union[JavaStatusResponse, BedrockStatusResponse, None] = function.status()

            if data is None:
                return None

            if isinstance(data, JavaStatusResponse):
                player_list: Union[list, str] = []
                players: Union[str, None] = data.players.sample

                if hasattr(data.players, 'sample') and data.players.sample is not None:
                    player_list = [{'name': player.name, 'id': player.id} for player in data.players.sample]

                if len(player_list) > 0:
                    players: list = MCServerData._get_players(player_list)
                    players: str = ', '.join(players)

                mod_info = data.raw.get('modinfo', {})
                mod_type = mod_info.get('type', None) if isinstance(mod_info, dict) else None
                mod_list: Union[list, str] = mod_info.get('modList', []) if isinstance(mod_info, dict) else []

                if len(mod_list) > 0:
                    mod_list = [f'&f&l{mod["modid"]} &8&l(&a&l{mod["version"]}&8&l)' for mod in mod_list]
                    mod_list: str = ', '.join(mod_list)

                else:
                    mod_list: str = 'No mods found'

                if self.bot:
                    bot_output: str = clean_output(
                        BotServerResponse(
                            ip_address=self.ip_address,
                            port=self.port,
                            version=str(data.version.protocol)
                        ).get_response()
                    )

                    # Get the bot color response
                    bot_output = BotUtilities.get_bot_color_response(bot_output)

                else:
                    bot_output: str = ''

                return JavaServerData(
                    ip_address=str(self.ip_address),
                    port=int(self.port),
                    motd=clean_output(data.description),
                    original_motd=data.description,
                    version=clean_output(data.version.name),
                    original_version=data.version.name,
                    protocol=str(data.version.protocol),
                    connected_players=str(data.players.online),
                    max_players=str(data.players.max),
                    players=players,
                    player_list=player_list,
                    mod=mod_type,
                    mods=mod_list,
                    favicon=data.favicon,
                    ping=int(data.latency),
                    bot_output=bot_output
                )

            elif isinstance(data, BedrockStatusResponse):
                bot_output: str = '&c&lIncompatible'

                return BedrockServerData(
                    ip_address=str(self.ip_address),
                    port=int(self.port),
                    motd=clean_output(data.description),
                    version=clean_output(data.version.name),
                    protocol=str(data.version.protocol),
                    connected_players=str(data.players.online),
                    max_players=str(data.players.max),
                    brand=data.version.brand,
                    map=clean_output(data.map),
                    gamemode=clean_output(data.gamemode),
                    ping=int(data.latency),
                    bot_output=bot_output
                )

        except (ConnectionRefusedError, TimeoutError, OSError, socket.gaierror):
            return None

    @staticmethod
    @logger.catch
    def _get_players(players: Union[list, None]) -> list:
        """
        Method to get the player names from the player list.
        :param players: The player list.
        :return: The player names.
        """
        return [player['name'] for player in players] if players is not None else []
