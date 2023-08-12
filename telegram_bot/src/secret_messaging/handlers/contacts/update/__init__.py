from aiogram import Dispatcher

from . import private_name, public_name, is_hidden

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    private_name.register_handlers(dispatcher)
    public_name.register_handlers(dispatcher)
    is_hidden.register_handlers(dispatcher)
