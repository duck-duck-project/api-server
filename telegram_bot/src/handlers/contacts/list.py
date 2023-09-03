from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ChatType

from repositories import ContactRepository
from repositories import HTTPClientFactory
from views.contacts import ContactListView
from views import answer_view

__all__ = ('register_handlers',)


async def on_show_contacts_list(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contacts = await contact_repository.get_by_user_id(message.from_user.id)
    view = ContactListView(contacts)
    await answer_view(message=message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_contacts_list,
        Text('👥 Контакты'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
