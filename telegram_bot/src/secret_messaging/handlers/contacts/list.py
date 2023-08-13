from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ChatType

from common.repositories import HTTPClientFactory
from common.views import answer_view, edit_message_by_view
from secret_messaging.repositories import ContactRepository
from secret_messaging.views import ContactListView

__all__ = ('register_handlers',)


async def on_show_contacts_list(
        message_or_callback_query: Message | CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contacts = await contact_repository.get_by_user_id(
            user_id=message_or_callback_query.from_user.id,
        )

    view = ContactListView(contacts)
    if isinstance(message_or_callback_query, Message):
        await answer_view(message=message_or_callback_query, view=view)
    else:
        await edit_message_by_view(
            message=message_or_callback_query.message,
            view=view,
        )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_show_contacts_list,
        Text('show-contacts-list'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
