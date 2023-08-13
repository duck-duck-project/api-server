from aiogram import Dispatcher

from . import (
    common,
    contacts,
    secret_messages,
    secret_medias,
    users,
    anonymous_messages,
)

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    common.register_handlers(dispatcher)
    contacts.register_handlers(dispatcher)
    secret_messages.register_handlers(dispatcher)
    secret_medias.register_handlers(dispatcher)
    users.register_handlers(dispatcher)
    anonymous_messages.register_handlers(dispatcher)
