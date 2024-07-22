from typing import Union
from loguru import logger
from ezjsonpy import translate_message

from mcptool.constants import MCPToolStrings, Emojis


class LanguageUtils:
    @staticmethod
    def get(key: str) -> Union[dict, list, str, int, float, None]:
        """
        Method to get the language value

        Args:
            key (Union[list, str]): The key to get the value from

        Returns:
            Union[dict, list, str, int, float, None]: The value of the key
        """

        value: Union[dict, list, str, int, float, None] = translate_message(key)

        if value is None or value == 'None':
            logger.error(f'Key {key} does not exist in the language file')
            return f'Key does not exist in the language file ({key})'

        if '%spaces%' in value:
            value = value.replace('%spaces%', MCPToolStrings.SPACES)

        if '%prefix%' in value:
            value = value.replace('%prefix%', MCPToolStrings.PREFIX)

        if '%timeEmoji%' in value:
            value = value.replace('%timeEmoji%', Emojis.TIME_EMOJI)

        return value
