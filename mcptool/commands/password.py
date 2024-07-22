import time

from ezjsonpy import get_config_value
from loguru import logger
from mccolors import mcwrite

from mcptool.commands.arguments.argument_validator import ValidateArgument
from mcptool.nordify.finder import NordifyFinder
from mcptool.utilities.language.utilities import LanguageUtils as LM
from mcptool.constants import URLS


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'password'
        self.command_arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]
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
    def execute(self, user_arguments: list) -> None:
        """
        Method to execute the command
        :param user_arguments: list: The arguments to execute the command
        """
        if not self.validate_arguments(user_arguments):
            return

        # Save user arguments
        username: str = user_arguments[0]
        api_username: str = get_config_value('nordifyAPI.username')
        api_password: str = get_config_value('nordifyAPI.password')

        if len(api_username) == 0 or len(api_password) == 0:
            mcwrite(LM.get('commands.password.invalidCredentials'))
            mcwrite(LM.get('commands.password.nordifyInfo').replace('%nordifyLink%', URLS.NORDIFY_DISCORD))
            return

        data = NordifyFinder(
            username=username,
            api_username=api_username,
            api_password=api_password
        ).get_user_data()

        if data is None:
            return

        if len(data) == 0:
            mcwrite(LM.get('commands.password.noResults').replace('%username%', username))
            return

        users_valid_passwords: list = []
        users_encrypted_passwords: list = []
        mcwrite(LM.get('commands.password.searching').replace('%username%', username))
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
            mcwrite(LM.get('commands.password.noResults').replace('%username%', username))
            return

        mcwrite(LM.get('commands.password.passwordsFound')
                .replace('%passwords%', str(passwords_found))
                .replace('%username%', username)
                )

    @staticmethod
    @logger.catch
    def show_user_data(user_data: dict) -> None:
        """
        Method to show the user data
        :param user_data: dict: The user data
        """
        if 'name' in user_data:
            if user_data['name'] is not None:
                mcwrite(LM.get('commands.password.data.username').replace('%username%', user_data['name']))

        if 'email' in user_data:
            if user_data['email'] is not None:
                mcwrite(LM.get('commands.password.data.username').replace('%email%', user_data['email']))

        if 'server' in user_data:
            if user_data['server'] is not None:
                server_text: str = LM.get('commands.password.data.server').replace('%server%', user_data['server'])

                if 'serverip' in user_data:
                    if user_data['serverip'] is not None:
                        server_text += f' &8(&b&l{user_data["serverip"]}&8)'

                mcwrite(server_text)

        if 'ip' in user_data:
            if user_data['ip'] is not None:
                if user_data['ip'].lower() != 'not found':
                    mcwrite(LM.get('commands.password.data.ip').replace('%ip%', user_data['ip']))

        if user_data['password'] is not None:
            password_color = '&a' if len(user_data['password']) < 32 else '&c&l'
            mcwrite(LM.get('commands.password.data.password').replace('%password%',
                                                                          f"{password_color}{user_data['password']}"))
        if 'salt' in user_data:
            if user_data['salt'] is not None:
                mcwrite(LM.get('commands.password.data.salt').replace('%salt%', user_data['salt']))
