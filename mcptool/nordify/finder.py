from typing import Union

import requests
from ezjsonpy import get_config_value, translate_message
from loguru import logger
from mccolors import mcwrite
from requests.auth import HTTPBasicAuth

from mcptool.constants import URLS
from mcptool.utilities.language.utilities import LanguageUtils as Lm


class NordifyFinder:
    def __init__(self, username: str, api_username: str, api_password: str):
        self.username: str = username
        self.api_username: str = api_username
        self.api_password: str = api_password
        self.error: bool = False

    def get_user_data(self) -> Union[dict, str, None]:
        response: Union[dict, None] = self.send_request()

        if self.error:
            return 'error'

        return response

    @logger.catch
    def send_request(self) -> Union[dict, None]:
        """
        Method to send the request to the API
        :return: dict: The response from the API
        """

        # Get the endpoint
        endpoint = f'{get_config_value("endpoints.nordifyAPI")}/name/{self.username}'

        # Send the request
        try:
            response: requests.Response = requests.get(
                url=endpoint,
                auth=HTTPBasicAuth(self.api_username, self.api_password),
                verify=False
            )
            json_response: dict = response.json()

        except (requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            mcwrite(Lm.get('commands.password.requestError'))
            logger.error(f'Error sending request to Nordify API: {e}')
            self.error = True
            return None

        # Check if the response was successful
        if response.status_code != 200:
            if 'message' in json_response:
                if self.username in json_response['message']:
                    mcwrite(Lm.get('commands.password.noResults').replace('%username%', self.username))
                    return None

            if 'error' in json_response:
                self.error = True

                if 'Authentication required' in json_response['error']:
                    mcwrite(Lm.get('commands.password.invalidCredentials'))
                    mcwrite(Lm.get('commands.password.nordifyInfo').replace('%nordifyLink%', URLS.NORDIFY_DISCORD))
                    return None

                logger.error(f'Error sending request to Nordify API: {json_response["error"]}')
                mcwrite(Lm.get('commands.password.requestError'))
                return None

        return json_response
