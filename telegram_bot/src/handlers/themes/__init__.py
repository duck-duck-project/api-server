from aiogram import Router

from . import list, errors

__all__ = ('router',)

router = Router(name=__name__)

list.register_handlers(router)
errors.register_handlers(router)
