from aiogram import Dispatcher
from aiogram.types import Update

from exceptions import SecretMessageDoesNotExistError

__all__ = ('register_handlers',)


async def on_secret_message_does_not_exist_error(
        update: Update,
        _: SecretMessageDoesNotExistError,
) -> bool:
    await update.callback_query.answer(
        'Сообщение не найдено. Возможно оно ещё не загружено на наши сервера.'
        ' Попробуйте через пару секунд',
        show_alert=True,
    )
    return True


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_secret_message_does_not_exist_error,
        exception=SecretMessageDoesNotExistError,
    )
