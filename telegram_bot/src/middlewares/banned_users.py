from aiogram.types import Update

from middlewares.common import Handler, ContextData, HandlerReturn
from models import User
from views import UserBannedInlineQueryView

__all__ = ('banned_users_middleware',)


async def banned_users_middleware(
        handler: Handler,
        event: Update,
        data: ContextData,
) -> HandlerReturn:
    user: User = data['user']
    if not user.is_banned:
        return await handler(event, data)

    text = 'Вы были заблокированы в боте и не можете его использовать'
    if event.message is not None:
        await event.message.reply(text)
    elif event.callback_query is not None:
        await event.callback_query.answer(show_alert=True)
    elif event.inline_query is not None:
        items = [
            UserBannedInlineQueryView()
            .get_inline_query_result_article()
        ]
        await event.inline_query.answer(items, is_personal=True)
