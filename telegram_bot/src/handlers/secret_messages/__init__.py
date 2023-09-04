from aiogram import Router

from . import direct, inverted, errors, create

__all__ = ('router',)

router = Router(name=__name__)

create.register_handlers(router)
errors.register_handlers(router)
inverted.register_handlers(router)
direct.register_handlers(router)
