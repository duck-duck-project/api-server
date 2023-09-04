from aiogram import Router

from . import delete, list, create, detail, update, errors

__all__ = ('router',)

router = Router(name=__name__)

errors.register_handlers(router)
delete.register_handlers(router)
list.register_handlers(router)
create.register_handlers(router)
detail.register_handlers(router)
update.register_handlers(router)
