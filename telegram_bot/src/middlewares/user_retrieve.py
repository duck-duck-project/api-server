from aiogram.enums import ChatType
from aiogram.types import Update

from exceptions import UserDoesNotExistError
from middlewares.common import Handler, ContextData, HandlerReturn
from services import extract_user_from_update

__all__ = ('user_retrieve_middleware',)


async def user_retrieve_middleware(
        handler: Handler,
        event: Update,
        data: ContextData,
) -> HandlerReturn:
    if event.message is not None:
        message = event.message
        is_chat_type_private = message.chat.type == ChatType.PRIVATE
        no_command = (
                message.text is not None
                and not message.text.startswith('/')
        )
        if no_command and not is_chat_type_private:
            return

    from_user = extract_user_from_update(event)

    user_repository = data['user_repository']
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
