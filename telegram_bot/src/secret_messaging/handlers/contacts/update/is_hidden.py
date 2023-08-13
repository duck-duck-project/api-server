from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ChatType

from common.repositories import HTTPClientFactory
from common.views import edit_message_by_view
from secret_messaging.callback_data import ContactUpdateCallbackData
from secret_messaging.repositories import ContactRepository
from secret_messaging.views import ContactDetailView

__all__ = ('register_handlers',)


async def on_toggle_is_hidden_status(
        callback_query: CallbackQuery,
        callback_data: dict,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    contact_id: int = callback_data['contact_id']

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contact = await contact_repository.get_by_id(contact_id)
        await contact_repository.update(
            contact_id=contact_id,
            public_name=contact.public_name,
            private_name=contact.private_name,
            is_hidden=not contact.is_hidden,
        )
        contact = await contact_repository.get_by_id(contact_id)

    view = ContactDetailView(contact)
    await edit_message_by_view(message=callback_query.message, view=view)
    await callback_query.answer('✅ Статус скрытости обновлен')


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_toggle_is_hidden_status,
        ContactUpdateCallbackData().filter(field='is_hidden'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
