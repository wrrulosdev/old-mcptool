from typing import Union

from ezjsonpy import translate_message
from loguru import logger

from ...constants import MCPToolStrings, Emojis, CLI


class LanguageUtils:
    @staticmethod
    def get(key: str) -> Union[dict, list, str, int, float, None]:
        """
        Method to get the value of a key from the language file
        :param key: Key to get the value from
        :return: The value of the key
        """
        value: Union[dict, list, str, int, float, None] = translate_message(key)

        if value is None or value == 'None':
            logger.error(f'Key {key} does not exist in the language file')
            return f'Key does not exist in the language file ({key})'

        if '%prefix%' in value:
            value = value.replace('%prefix%', MCPToolStrings.PREFIX)

        if '%timeEmoji%' in value:
            value = value.replace('%timeEmoji%', Emojis.TIME_EMOJI)

        if CLI.value and '%spaces%' in value:
            value = value.replace('%spaces%', '')
            return value

        if '%spaces%' in value:
            value = value.replace('%spaces%', MCPToolStrings.SPACES)

        return value
