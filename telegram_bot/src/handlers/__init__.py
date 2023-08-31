from aiogram import Dispatcher

from . import (
    common,
    server,
    countdown,
    contacts,
    secret_messages,
    secret_medias,
    teams,
    team_members,
    users,
    anonymous_messages,
    premium,
)

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    common.register_handlers(dispatcher)
    countdown.register_handlers(dispatcher)
    contacts.register_handlers(dispatcher)
    secret_messages.register_handlers(dispatcher)
    secret_medias.register_handlers(dispatcher)
    teams.register_handlers(dispatcher)
    team_members.register_handlers(dispatcher)
    users.register_handlers(dispatcher)
    premium.register_handlers(dispatcher)
    anonymous_messages.register_handlers(dispatcher)
    server.register_handlers(dispatcher)
