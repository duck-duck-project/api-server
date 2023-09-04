from aiogram import Router

from . import create, detail

__all__ = ('router',)

router = Router(name=__name__)

create.register_handlers(router)
detail.register_handlers(router)
