from aiogram import Dispatcher

from . import direct, inverted, errors, create

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    create.register_handlers(dispatcher)
    errors.register_handlers(dispatcher)
    direct.register_handlers(dispatcher)
    inverted.register_handlers(dispatcher)
