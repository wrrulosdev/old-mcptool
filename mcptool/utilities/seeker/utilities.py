import http.server
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Union

import requests
from ezjsonpy import get_config_value, set_config_value
from loguru import logger
from mccolors import mcwrite

from ...inputcustom import Input
from ...minecraft.server import JavaServerData, BedrockServerData
from ...minecraft.server.server_data import ServerData
from ...minecraft.server.show_server import ShowMinecraftServer
from ...utilities.language.utilities import LanguageUtils as Lm


# Token Handler
class TokenHandler(BaseHTTPRequestHandler):
    token = None
    token_received_event = None

    @classmethod
    def initialize(cls, token_event: threading.Event) -> None:
        """
        Method to initialize the token handler
        :param token_event: threading.Event: The event to indicate that the token has been received
        """
        cls.token_received_event = token_event

    def do_GET(self) -> None:
        """Method to handle the GET request"""
        if '?api_key=' in self.path:
            TokenHandler.token = self.path.split('=')[1]
            mcwrite(Lm.get('commands.seeker.token.tokenObtained'))
            logger.info('Token obtained from the seeker')
            set_config_value('seekerToken', TokenHandler.token)
            TokenHandler.token_received_event.set()
            self.server.shutdown()

    @staticmethod
    @logger.catch
    def valid_token(token: str) -> bool:
        """
        Method to validate the token
        :param token: Seeker Token
        :return: True if the token is valid, False otherwise
        """
        url: str = f"{get_config_value('endpoints.seekerAPI')}/user_info"
        headers: dict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data: dict = {
            "ip": "127.0.0.1",
            "port": 25565,
            'api_key': token
        }

        try:
            response: requests.Response = requests.post(url, headers=headers, json=data)

            if response.status_code != 200:
                return False

            return True

        except (requests.ConnectionError, requests.Timeout) as e:
            mcwrite(Lm.get('errors.endpointConnectionError'))
            logger.warning(f'Error connecting to the endpoint: {url} - {data} - {e}')
            return False


# Server Manager
class ServerManager:
    @staticmethod
    def start_server(token_event: threading.Event) -> None:
        """
        Method to start the server
        :param token_event: threading.Event: The event to indicate that the token has been received
        :return: None
        """
        TokenHandler.initialize(token_event)

        try:
            server: http.server.HTTPServer = HTTPServer(('localhost', 7637), TokenHandler)
            server.serve_forever()
        except OSError:
            mcwrite(Lm.get('commands.seeker.token.restart'))
            logger.error('Server encountered an OSError and will restart.')
            token_event.set()


class SeekerServers:
    @staticmethod
    @logger.catch
    def get_servers() -> dict:
        """
        Method to get the servers from the seeker API
        :return: dict: The list of servers
        """
        token: str = get_config_value('seekerToken')

        if token is None:
            mcwrite(Lm.get('commands.seeker.token.invalidToken'))
            return []

        if not TokenHandler.valid_token(token):
            mcwrite(Lm.get('commands.seeker.token.invalidToken'))

        # Get server data to send the request
        data: dict = SeekerServers.create_server_data()
        # Send the request
        servers: Union[dict, None] = SeekerServers.send_request(
            url=f"{get_config_value('endpoints.seekerAPI')}/servers",
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            data=data
        )

        if servers is None:
            return {}

        return servers

    @staticmethod
    @logger.catch
    def create_server_data() -> dict:
        """
        Method to get the servers from the seeker API
        :return: The data to send the request
        """
        data: dict = {
            'api_key': get_config_value('seekerToken')
        }

        # Search options
        country_code: Union[str, None] = None
        cracked: Union[bool, None] = None
        description: Union[str, None] = None
        only_bungee_spoofable: Union[bool, None] = None
        protocol: Union[int, None] = None
        online_players: Union[int, None] = None

        # Ask the user if they want to filter the servers
        filter: Union[bool, None] = Input(
            input_message=Lm.get('commands.seeker.servers.filterByData'),
            input_type='boolean'
        ).get_input()

        if filter is None or not filter:
            return data

        filter_country_code: Union[bool, None] = Input(
            input_message=Lm.get('commands.seeker.servers.filterByCountryCode'),
            input_type='boolean'
        ).get_input()

        if filter_country_code is not None:
            if filter_country_code:
                country_code = Input(
                    input_message=Lm.get('commands.seeker.servers.filterByCountryCodeText'),
                    input_type='country_code'
                ).get_input()

        filter_cracked: Union[bool, None] = Input(
            input_message=Lm.get('commands.seeker.servers.filterByCracked'),
            input_type='boolean'
        ).get_input()

        if filter_cracked is not None:
            cracked = filter_cracked

        filter_description: Union[bool, None] = Input(
            input_message=Lm.get('commands.seeker.servers.filterByDescription'),
            input_type='boolean'
        ).get_input()

        if filter_description is not None:
            if filter_description:
                description = Input(
                    input_message=Lm.get('commands.seeker.servers.filterByDescriptionText'),
                    input_type='string'
                ).get_input()

        filter_only_bungee_spoofable: Union[bool, None] = Input(
            input_message=Lm.get('commands.seeker.servers.filterByOnlyBungeespoofable'),
            input_type='boolean'
        ).get_input()

        if filter_only_bungee_spoofable is not None:
            only_bungee_spoofable = filter_only_bungee_spoofable

        filter_protocol: Union[bool, None] = Input(
            input_message=Lm.get('commands.seeker.servers.filterByProtocol'),
            input_type='boolean'
        ).get_input()

        if filter_protocol is not None:
            if filter_protocol:
                protocol = Input(
                    input_message=Lm.get('commands.seeker.servers.filterByProtocolText'),
                    input_type='integer'
                ).get_input()

        filter_online_players: Union[bool, None] = Input(
            input_message=Lm.get('commands.seeker.servers.filterByOnlinePlayers'),
            input_type='boolean'
        ).get_input()

        if filter_online_players is not None:
            if filter_online_players:
                online_players = Input(
                    input_message=Lm.get('commands.seeker.servers.filterByOnlinePlayersText'),
                    input_type='integer'
                ).get_input()

        if country_code is not None:
            data['country_code'] = country_code

        if cracked is not None and cracked:
            data['cracked'] = cracked

        if description is not None:
            data['description'] = description

        if only_bungee_spoofable is not None:
            data['only_bungeespoofable'] = only_bungee_spoofable

        if protocol is not None:
            data['protocol'] = protocol

        if online_players is not None:
            data['online_players'] = online_players

        return data

    @staticmethod
    @logger.catch
    def send_request(url: str, headers: dict, data: dict) -> Union[dict, None]:
        """
        Method to send the request to the seeker API
        :param url: Seeker API URL
        :param headers: Headers
        :param data: Data to send
        :return: The response from the API; None if the request failed
        """
        try:
            logger.info(f'''
Getting servers from the seeker API...

 ↪ URL: {url}
 ↪ Headers: {headers}
 ↪ Data: {data}''')

            mcwrite(Lm.get('commands.seeker.servers.sendingRequest'))
            response = requests.post(url, headers=headers, json=data)

            if response.status_code != 200:
                logger.error(f'Error getting the servers from the seeker API: {response.json()}')
                return None

            if 'data' not in response.json():
                logger.error(f'Error getting the servers from the seeker API (data value not found): {response.json()}')
                return None

            return response.json()['data']

        except (
                requests.ConnectionError, requests.Timeout, requests.exceptions.RequestException,
                UnicodeDecodeError) as e:
            mcwrite(Lm.get('errors.endpointConnectionError'))
            logger.warning(f'Error connecting to the endpoint: {url} - {data} - {e}')
            return None

        except Exception as e:
            mcwrite(Lm.get('errors.endpointConnectionError'))
            logger.error(f'Error getting the servers from the seeker API: {e}')
            return None


class SeekerUtilities:
    def __init__(self):
        self.threads: list[Union[threading.Thread, None]] = []
        self.stopped: bool = False
        self.semaphore: threading.Semaphore = threading.Semaphore(10)

    @logger.catch
    def get_token(self) -> bool:
        """
        Method to get the token from the user
        and save it in the settings.
        """
        error: bool = False

        # Check if the endpoint is valid
        if get_config_value('endpoints.seeker') is None:
            mcwrite(Lm.get('errors.invalidEndpoint'))
            logger.error(f'Invalid endpoint for seeker: {get_config_value("endpoints.seeker")}')

        # Event to indicate that the token has been received
        token_received: threading.Event = threading.Event()
        mcwrite(Lm.get('commands.seeker.token.gettingToken'))
        server_thread: threading.Thread = threading.Thread(target=ServerManager.start_server, args=(token_received,))
        server_thread.start()
        time.sleep(1)

        if not error:
            webbrowser.open(get_config_value('endpoints.seeker'))

        token_received.wait()
        return True

    @logger.catch
    def get_servers(self) -> bool:
        """
        Method to get the servers from the seeker API.
        """
        token: str = get_config_value('seekerToken')

        if token is None:
            mcwrite(Lm.get('commands.seeker.token.invalidToken'))
            return False

        if not TokenHandler.valid_token(token):
            mcwrite(Lm.get('commands.seeker.token.invalidToken'))
            return False

        # Get the servers
        servers = SeekerServers.get_servers()

        if len(servers) == 0:
            mcwrite(Lm.get('commands.seeker.servers.noServers'))
            return False

        mcwrite(Lm.get('commands.seeker.servers.gettingServers'))

        # Print the servers
        for server in servers:
            if 'server' not in server:
                continue

            server_thread = threading.Thread(target=self.get_server_data, args=(server['server'],))
            server_thread.start()
            self.threads.append(server_thread)

        for thread in self.threads:
            thread.join()

        return True

    @logger.catch
    def get_server_data(self, server) -> None:
        """
        Get the server data and show it.
        :param server: The server to get the data
        """
        with self.semaphore:
            try:
                server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(server).get_data()

                if self.stopped:
                    return

                if server_data is None:
                    return

                ShowMinecraftServer.show(server_data=server_data)

            except KeyboardInterrupt:
                self.stopped = True
                return
