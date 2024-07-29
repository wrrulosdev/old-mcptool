import threading
import time
from typing import Union

from loguru import logger
from mccolors import mcwrite

from ..inputcustom import Input
from ..scrappers.minecraftservers import MinecraftServerScrapper
from ..utilities.language.utilities import LanguageUtils as Lm


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'websearch'
        self.command_arguments: list = [i for i in Lm.get(f'commands.{self.name}.arguments')]

    @logger.catch
    def execute(self, user_arguments: list, scrapper: MinecraftServerScrapper) -> bool:
        """
        Method to execute the command
        :param scrapper: The scrapper object
        :param user_arguments: The arguments to execute the command
        """
        filter_data = Input(
            input_message=Lm.get('commands.websearch.filterByData'),
            input_type='boolean'
        ).get_input()

        if filter_data is None:
            return False

        if filter_data:
            filter_only_bot_join: Union[bool, None] = Input(
                input_message=Lm.get('commands.websearch.filterByOnlyBotCanJoin'),
                input_type='boolean'
            ).get_input()

            if filter_only_bot_join is not None:
                scrapper.filters['onlyBotCanJoin'] = filter_only_bot_join

            filter_description: Union[str, None] = Input(
                input_message=Lm.get('commands.websearch.filterByDescription'),
                input_type='string'
            ).get_input()

            if filter_description is not None:
                if filter_description:
                    scrapper.filters['filterByDescription'] = filter_description
                    scrapper.filters['description'] = Input(
                        input_message=Lm.get('commands.websearch.filterByDescriptionText'),
                        input_type='string'
                    ).get_input()

            filter_online_players: Union[int, None] = Input(
                input_message=Lm.get('commands.websearch.filterByOnlinePlayers'),
                input_type='integer'
            ).get_input()

            if filter_online_players is not None:
                if filter_online_players:
                    scrapper.filters['filterByOnlinePlayers'] = filter_online_players
                    scrapper.filters['onlinePlayers'] = Input(
                        input_message=Lm.get('commands.websearch.filterByOnlinePlayersText'),
                        input_type='integer'
                    ).get_input()

            filter_protocol: Union[int, None] = Input(
                input_message=Lm.get('commands.websearch.filterByProtocol'),
                input_type='integer'
            ).get_input()

            if filter_protocol is not None:
                if filter_protocol:
                    scrapper.filters['filterByProtocol'] = filter_protocol
                    scrapper.filters['protocol'] = Input(
                        input_message=Lm.get('commands.websearch.filterByProtocolText'),
                        input_type='integer'
                    ).get_input()

            mcwrite(Lm.get('commands.websearch.filterDataShow')
                    .replace('%onlyBotCanJoin%', '✔️' if scrapper.filters['onlyBotCanJoin'] else '❌')
                    .replace('%description%',
                             scrapper.filters['description'] if scrapper.filters['filterByDescription'] else '❌')
                    .replace('%onlinePlayers%', str(scrapper.filters['onlinePlayers']) if scrapper.filters[
                'filterByOnlinePlayers'] else '❌')
                    .replace('%protocol%',
                             str(scrapper.filters['protocol']) if scrapper.filters['filterByProtocol'] else '❌')
                    )

        # It seems strange, but it's the only way I found to control thread closing the way I want.
        # If you're reading this and think you know better, let me know or make a pull request! :D
        scrapper_thread = threading.Thread(target=scrapper.get)
        scrapper_thread.start()

        try:
            while True:
                time.sleep(0.1)

        except KeyboardInterrupt:
            scrapper.stop()
            mcwrite(Lm.get('commands.ctrlC'))
            scrapper_thread.join()
            scrapper.restore()

        return True
