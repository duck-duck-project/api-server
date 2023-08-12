from aiogram import Dispatcher

from . import create, detail

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    create.register_handlers(dispatcher)
    detail.register_handlers(dispatcher)
