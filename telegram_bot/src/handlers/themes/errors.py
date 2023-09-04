from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Update

from exceptions import ThemeDoesNotExistError

__all__ = ('register_handlers',)


async def on_theme_does_not_exist_error(
        update: Update,
        _: ThemeDoesNotExistError,
) -> bool:
    await update.message.reply('Тема не найдена')
    return True


def register_handlers(router: Router) -> None:
    router.errors.register(
        on_theme_does_not_exist_error,
        ExceptionTypeFilter(ThemeDoesNotExistError),
    )
