import re

from aiogram.types import Message

__all__ = ('theme_update_command_filter',)

pattern = re.compile(r'^/theme_\d+$')


def theme_update_command_filter(message: Message) -> bool | dict:
    if message.text is None:
        return False
    match = pattern.search(message.text)
    if match:
        theme_id: int = int(match.string.split('_')[1])
        return {'theme_id': theme_id}
    return False
