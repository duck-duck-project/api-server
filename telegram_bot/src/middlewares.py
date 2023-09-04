from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import Update

from exceptions import UserDoesNotExistError
from repositories import HTTPClientFactory, UserRepository

__all__ = (
    'UserMiddleware',
)


class UserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any]
    ) -> Any:
        if event.message is not None:
            message = event.message
            is_chat_type_private = message.chat.type == ChatType.PRIVATE
            no_command = (
                    message.text is not None
                    and not message.text.startswith('/')
            )
            if no_command and not is_chat_type_private:
                return

        if event.message is not None:
            from_user = event.message.from_user
        elif event.callback_query is not None:
            from_user = event.callback_query.from_user
        elif event.inline_query is not None:
            from_user = event.inline_query.from_user
        elif event.chosen_inline_result is not None:
            from_user = event.chosen_inline_result.from_user
        else:
            raise ValueError('Unknown event type')

        closing_http_client_factory: HTTPClientFactory = (
            data['closing_http_client_factory']
        )
        async with closing_http_client_factory() as http_client:
            user_repository = UserRepository(http_client)
            try:
                user = await user_repository.get_by_id(from_user.id)
            except UserDoesNotExistError:
                user = await user_repository.create(
                    user_id=from_user.id,
                    fullname=from_user.full_name,
                    username=from_user.username,
                )
            data['user'] = user
        return await handler(event, data)

# class BannedUsersFilterMiddleware(BaseMiddleware):
#     skip_patterns = ('update', 'error')
#
#     async def pre_process(
#             self,
#             obj: Message | CallbackQuery | InlineQuery,
#             data: dict,
#             *args,
#     ) -> None:
#         if isinstance(obj, Message):
#             if obj.get_command() is None:
#                 return
#
#         user: User = data['user']
#         text = 'Вы были заблокированы в боте и не можете его использовать'
#         if user.is_banned:
#             match obj:
#                 case Message():
#                     await obj.answer(text)
#                 case CallbackQuery():
#                     await obj.answer(text, show_alert=True)
#                 case InlineQuery():
#                     items = [
#                         UserBannedInlineQueryView()
#                         .get_inline_query_result_article()
#                     ]
#                     await obj.answer(items, is_personal=True)
#             raise CancelHandler
