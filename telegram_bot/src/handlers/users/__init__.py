from aiogram import Router

from . import update, detail

__all__ = ('router',)

router = Router()

update.register_handlers(router)
detail.register_handlers(router)
