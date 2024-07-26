import requests

from typing import Union
from loguru import logger

from mcptool.minecraft.server import JavaServerData, BedrockServerData, clean_output
from mcptool.minecraft.bot.server_response import BotServerResponse
from mcptool.utilities.minecraft.bot.utilities import BotUtilities


class MCStatusIOAPI:
    def __init__(self, target: str, bot: bool = True) -> None:
        self.target = target
        self.bot = bot
        self.java_endpoint: str = 'https://api.mcstatus.io/v2/status/java/'
        self.bedrock_endpoint: str = 'https://api.mcstatus.io/v2/status/bedrock/'

    @logger.catch
    def get(self) -> Union[JavaServerData, BedrockServerData, None]:
        """
        Method to get the server data from the MCStatus.io API.
        :return: The server data if the server is online, otherwise None
        """
        data: Union[JavaServerData, None] = self._send_java_request()

        if data is None:
            data: Union[BedrockServerData, None] = self._send_bedrock_request()

        # If the data is still None, return None
        if data is None:
            return None

        return data

    @logger.catch
    def _send_java_request(self) -> Union[JavaServerData, None]:
        """
        Method to send the request to the MCStatus.io API.
        :return: The server data if the server is online, otherwise None
        """
        try:
            response: requests.Response = requests.get(f'{self.java_endpoint}{self.target}')

            if response.status_code != 200:
                return None

            data: Union[JavaServerData, None] = self._convert_data(data=response.json(), server_type='java')
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending the request to the MCStatus.io API (Java): {e}")
            return None

    @logger.catch
    def _send_bedrock_request(self) -> Union[BedrockServerData, None]:
        """
        Method to send the request to the MCStatus.io API.
        :return: The server data if the server is online, otherwise None
        """
        try:
            response: requests.Response = requests.get(f'{self.bedrock_endpoint}{self.target}')

            if response.status_code != 200:
                return None

            data: Union[BedrockServerData, None] = self._convert_data(data=response.json(), server_type='bedrock')
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending the request to the MCStatus.io API (Bedrock): {e}")
            return None

    @logger.catch
    def _convert_data(self, data: dict, server_type: str) -> Union[JavaServerData, BedrockServerData, None]:
        """
        Method to convert the data from the API to the server data class.
        :param data:  The data from the API
        :param server_type:  The server type
        :return: The server data if the server is online, otherwise None
        """
        player_list: list = []
        players_str: Union[str, None] = None

        if not data['online']:
            return None

        if server_type == 'java':
            if data['players']['list'] is not None:
                player_list: list = [{'name_raw': player['name_raw'], 'uuid': player['uuid']} for player in data['players']['list']]

                # Replace 'name_raw' for 'name' and 'uuid for 'id
                for player in player_list:
                    player['name'] = player.pop('name_raw')
                    player['id'] = player.pop('uuid')

                if len(player_list) > 0:
                    players: list = self._get_players(player_list)
                    players_str: str = ', '.join(players)

                ip_address: str = data['ip_address'] if data['ip_address'] is not None else data['host']
                port: int = data['srv_record']['port'] if data['srv_record'] is not None else data['port']
                motd: str = clean_output(data['motd']['raw'])
                original_motd: str = data['motd']['raw']
                version: str = clean_output(data['version']['name_raw'])
                original_version: str = data['version']['name_raw']
                protocol: str = data['version']['protocol']
                connected_players: str = data['players']['online']
                max_players: str = data['players']['max']
                players: str = players_str
                mod: Union[str, None] = None
                mods: list = []
                favicon: Union[str, None] = data['icon']
                ping: Union[int, None] = None

                if self.bot:
                    if ':' in self.target:
                        bot_output: str = clean_output(BotServerResponse(ip_address, port, protocol).get_response())

                    else:
                        bot_output: str = clean_output(BotServerResponse(self.target, 25565, protocol).get_response())

                    # Get the bot color response
                    bot_output = BotUtilities.get_bot_color_response(bot_output)

                else:
                    bot_output: str = ''

                return JavaServerData(
                    ip_address=ip_address,
                    port=port,
                    motd=motd,
                    original_motd=original_motd,
                    version=version,
                    original_version=original_version,
                    protocol=protocol,
                    connected_players=connected_players,
                    max_players=max_players,
                    players=players,
                    player_list=player_list,
                    mod=mod,
                    mods=mods,
                    favicon=favicon,
                    ping=ping,
                    bot_output=bot_output
                )

        if server_type == 'bedrock':
            bot_output: str = '&c&lIncompatible'
            ip_address: str = data['ip_address']
            port: int = data['port']
            motd: str = clean_output(data['motd']['raw'])
            version: str = clean_output(data['version']['name'])
            protocol: str = data['version']['protocol']
            connected_players: str = data['players']['online']
            max_players: str = data['players']['max']
            brand: Union[str, None] = None
            map: Union[str, None] = None
            gamemode: Union[str, None] = data['gamemode']
            ping: Union[int, None] = None

            return BedrockServerData(
                ip_address=ip_address,
                port=port,
                motd=motd,
                version=version,
                protocol=protocol,
                connected_players=connected_players,
                max_players=max_players,
                brand=brand,
                map=map,
                gamemode=gamemode,
                ping=ping,
                bot_output=bot_output
            )

        return None

    @logger.catch
    def _get_players(self, players: Union[list, None]) -> list:
        """
        Method to get the players from the list.
        :param players: The list of players
        :return: The list of players
        """
        return [player['name'] for player in players] if players is not None else []
