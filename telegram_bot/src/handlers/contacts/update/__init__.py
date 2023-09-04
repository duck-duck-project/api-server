from aiogram import Router

from . import private_name, public_name, is_hidden

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    private_name.register_handlers(router)
    public_name.register_handlers(router)
    is_hidden.register_handlers(router)
