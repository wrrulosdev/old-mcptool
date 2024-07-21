from loguru import logger


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'clear'

    @logger.catch
    def execute(self, arguments: list = []) -> None:
        """
        Method to execute the command
        :param arguments: list: The arguments to execute the command
        """

        pass