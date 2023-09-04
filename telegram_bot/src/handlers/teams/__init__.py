from aiogram import Router

from . import list, detail, create, delete

__all__ = ('router',)

router = Router(name=__name__)

list.register_handlers(router)
detail.register_handlers(router)
create.register_handlers(router)
delete.register_handlers(router)
