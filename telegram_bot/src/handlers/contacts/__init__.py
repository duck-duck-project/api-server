from aiogram import Dispatcher

from . import delete, list, create, detail, update

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    delete.register_handlers(dispatcher)
    list.register_handlers(dispatcher)
    create.register_handlers(dispatcher)
    detail.register_handlers(dispatcher)
    update.register_handlers(dispatcher)
