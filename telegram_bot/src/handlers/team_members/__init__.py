from aiogram import Dispatcher

from . import list, create

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    list.register_handlers(dispatcher)
    create.register_handlers(dispatcher)
