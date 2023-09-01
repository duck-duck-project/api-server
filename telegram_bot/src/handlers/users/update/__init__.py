from aiogram import Dispatcher

from . import can_be_added_to_contacts, can_receive_notifications, theme

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    can_be_added_to_contacts.register_handlers(dispatcher)
    can_receive_notifications.register_handlers(dispatcher)
    theme.register_handlers(dispatcher)
