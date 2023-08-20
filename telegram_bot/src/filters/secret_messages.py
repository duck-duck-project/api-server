from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ChosenInlineResult

__all__ = ('SecretMessageValidFormatChosenInlineResultFilter',)


class SecretMessageValidFormatChosenInlineResultFilter(BoundFilter):
    key = 'secret_message_valid_format'

    async def check(
            self,
            chosen_inline_result: ChosenInlineResult,
    ) -> bool | dict:
        try:
            _, contact_id = chosen_inline_result.result_id.split('@')
            return {'contact_id': int(contact_id)}
        except ValueError:
            return False
