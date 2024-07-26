from mcptool.utilities.language.utilities import LanguageUtils as Lm


class CommandFinishedMessage:
    def __init__(self, command_time) -> None:
        self.time: float = command_time

    def get_message(self) -> str:
        """
        Method to get the finished message
        :return: The message
        """
        if self.time < 60:
            return Lm.get('commands.commandFinishedIn.seconds').replace('%seconds%', str(round(self.time)))

        if self.time < 3600:
            minutes = round(self.time / 60)
            seconds = round(self.time % 60)
            return Lm.get('commands.commandFinishedIn.minutes').replace('%minutes%', str(minutes)).replace('%seconds%', str(seconds))

        if self.time < 86400:
            hours = round(self.time / 3600)
            minutes = round((self.time % 3600) / 60)
            seconds = round((self.time % 3600) % 60)
            return Lm.get('commands.commandFinishedIn.hours').replace('%hours%', str(hours)).replace('%minutes%', str(minutes)).replace('%seconds%', str(seconds))

        days = round(self.time / 86400)
        hours = round((self.time % 86400) / 3600)
        minutes = round(((self.time % 86400) % 3600) / 60)
        seconds = round(((self.time % 86400) % 3600) % 60)
        return Lm.get('commands.commandFinishedIn.days').replace('%days%', str(days)).replace('%hours%', str(hours)).replace('%minutes%', str(minutes)).replace('%seconds%', str(seconds))
