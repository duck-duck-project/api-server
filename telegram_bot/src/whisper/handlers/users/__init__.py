from aiogram import Dispatcher

from . import update, detail

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    update.register_handlers(dispatcher)
    detail.register_handlers(dispatcher)
