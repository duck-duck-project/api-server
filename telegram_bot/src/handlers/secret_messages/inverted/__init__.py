from aiogram import Dispatcher

from . import create, detail

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    detail.register_handlers(dispatcher)
    create.register_handlers(dispatcher)
