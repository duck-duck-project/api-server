from aiogram import Dispatcher
from aiogram.types import Update

from exceptions import ThemeDoesNotExistError

__all__ = ('register_handlers',)


async def on_theme_does_not_exist_error(
        update: Update,
        _: ThemeDoesNotExistError,
) -> bool:
    await update.message.reply('Тема не найдена')
    return True


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_theme_does_not_exist_error,
        exception=ThemeDoesNotExistError,
    )
