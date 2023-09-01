from aiogram import Dispatcher

from . import list, errors

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    list.register_handlers(dispatcher)
    errors.register_handlers(dispatcher)
