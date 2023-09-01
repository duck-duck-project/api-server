import re

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

__all__ = ('ThemeUpdateCommandFilter',)


class ThemeUpdateCommandFilter(BoundFilter):
    key = 'theme_update_command'
    pattern = re.compile(r'^/theme_\d+$')

    async def check(self, message: Message) -> bool | dict:
        match = self.pattern.search(message.text)
        if match:
            theme_id: int = int(match.string.split('_')[1])
            return {'theme_id': theme_id}
        return False
