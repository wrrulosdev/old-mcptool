import time
from typing import Union

from ezjsonpy import get_config_value
from loguru import logger
from mccolors import mcwrite

from ..commands.arguments.argument_validator import ValidateArgument
from ..constants import URLS
from ..nordify.finder import NordifyFinder
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.api_username: Union[str, None] = None
        self.api_password: Union[str, None] = None
        self.name: str = 'password'
        self.command_arguments: list = [i for i in Lm.get(f'commands.{self.name}.arguments')]
        logger.debug(f"Command initialized: {self.name}, arguments: {self.command_arguments}")

    @logger.catch
    def validate_arguments(self, user_arguments: list) -> bool:
        """
        Method to validate the arguments
        :param user_arguments: list: The arguments to validate
        :return: bool: True if the arguments are valid, False otherwise
        """
        if not ValidateArgument.validate_arguments_length(
                command_name=self.name,
                command_arguments=self.command_arguments,
                user_arguments=user_arguments
        ):
            return False

        return True

    @logger.catch
    def execute(self, user_arguments: list) -> bool:
        """
        Method to execute the command
        :param user_arguments: list: The arguments to execute the command
        """
        if not self.validate_arguments(user_arguments):
            return False

        # Get the first 10 arguments
        user_arguments = user_arguments[:10]

        # Save user arguments
        self.api_username: str = get_config_value('nordifyAPI.username', 'nordify')
        self.api_password: str = get_config_value('nordifyAPI.password', 'nordify')

        if len(self.api_username) == 0 or len(self.api_password) == 0:
            mcwrite(Lm.get('commands.password.invalidCredentials'))
            mcwrite(Lm.get('commands.password.nordifyInfo').replace('%nordifyLink%', URLS.NORDIFY_DISCORD))
            return False

        for username in user_arguments:
            error: bool = self.search_user(username)

            if error:
                return False

        return True

    def search_user(self, username: str) -> bool:
        """
        Method to search for a user
        :param username:
        :return: True if there was an error, False otherwise
        """

        data = NordifyFinder(
            username=username,
            api_username=self.api_username,
            api_password=self.api_password
        ).get_user_data()

        if data is None:
            return False

        if isinstance(data, str) and data == 'error':
            return True

        if len(data) == 0:
            mcwrite(Lm.get('commands.password.noResults').replace('%username%', username))
            return False

        users_valid_passwords: list = []
        users_encrypted_passwords: list = []
        mcwrite(Lm.get('commands.password.searching').replace('%username%', username))
        time.sleep(0.5)

        for username_data in data:
            normalized_username = {k.lower(): v for k, v in username_data.items()}

            if 'password' not in normalized_username:
                continue

            if normalized_username['password'] is not None:
                if normalized_username['password'] == 'null':
                    continue

                if len(normalized_username['password']) < 32:
                    users_valid_passwords.append(normalized_username)
                else:
                    users_encrypted_passwords.append(normalized_username)

        for user in users_valid_passwords:
            self.show_user_data(user)

        for user in users_encrypted_passwords:
            self.show_user_data(user)

        passwords_found: int = len(users_valid_passwords) + len(users_encrypted_passwords)

        if passwords_found == 0:
            mcwrite(Lm.get('commands.password.noResults').replace('%username%', username))
            return False

        mcwrite(Lm.get('commands.password.passwordsFound')
                .replace('%passwords%', str(passwords_found))
                .replace('%username%', username)
                )

        return False

    @staticmethod
    @logger.catch
    def show_user_data(user_data: dict) -> None:
        """
        Method to show the user data
        :param user_data: dict: The user data
        """
        if 'name' in user_data:
            if user_data['name'] is not None:
                mcwrite(Lm.get('commands.password.data.username').replace('%username%', user_data['name']))

        if 'email' in user_data:
            if user_data['email'] is not None:
                mcwrite(Lm.get('commands.password.data.username').replace('%email%', user_data['email']))

        if 'server' in user_data:
            if user_data['server'] is not None:
                server_text: str = Lm.get('commands.password.data.server').replace('%server%', user_data['server'])

                if 'serverip' in user_data:
                    if user_data['serverip'] is not None:
                        server_text += f' &8(&b&l{user_data["serverip"]}&8)'

                mcwrite(server_text)

        if 'ip' in user_data:
            if user_data['ip'] is not None:
                if user_data['ip'].lower() != 'not found':
                    mcwrite(Lm.get('commands.password.data.ip').replace('%ip%', user_data['ip']))

        if user_data['password'] is not None:
            password_color = '&a' if len(user_data['password']) < 32 else '&c&l'
            mcwrite(Lm.get('commands.password.data.password').replace('%password%',
                                                                      f"{password_color}{user_data['password']}"))
        if 'salt' in user_data:
            if user_data['salt'] is not None:
                mcwrite(Lm.get('commands.password.data.salt').replace('%salt%', user_data['salt']))
