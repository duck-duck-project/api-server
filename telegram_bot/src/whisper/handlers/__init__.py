from aiogram import Dispatcher

from . import contacts, secret_messages, secret_medias, users

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    contacts.register_handlers(dispatcher)
    secret_messages.register_handlers(dispatcher)
    secret_medias.register_handlers(dispatcher)
    users.register_handlers(dispatcher)
