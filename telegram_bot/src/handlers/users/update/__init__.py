from aiogram import Router

from . import can_be_added_to_contacts, can_receive_notifications, theme

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    can_be_added_to_contacts.register_handlers(router)
    can_receive_notifications.register_handlers(router)
    theme.register_handlers(router)
