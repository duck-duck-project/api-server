from aiogram import Router

from . import create, detail

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    detail.register_handlers(router)
    create.register_handlers(router)
