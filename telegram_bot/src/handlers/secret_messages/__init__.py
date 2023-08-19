from aiogram import Dispatcher

from . import direct, inverted, errors

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    errors.register_handlers(dispatcher)
    direct.register_handlers(dispatcher)
    inverted.register_handlers(dispatcher)
