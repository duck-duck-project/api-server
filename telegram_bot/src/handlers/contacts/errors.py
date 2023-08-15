from aiogram import Dispatcher
from aiogram.types import Update

from exceptions import ContactDoesNotExistError

__all__ = ('register_handlers',)


async def on_contact_does_not_exist_error(
        update: Update,
        exception: ContactDoesNotExistError,
) -> bool:
    text = '😔 Контакт не существует или был удален'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    return True


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_contact_does_not_exist_error,
        exception=ContactDoesNotExistError,
    )
