from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ChatType

from callback_data import ContactDeleteCallbackData
from repositories import ContactRepository
from repositories import HTTPClientFactory
from views import ContactListView
from views import edit_message_by_view

__all__ = ('register_handlers',)


async def on_delete_contact(
        callback_query: CallbackQuery,
        callback_data: dict,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    contact_id: int = callback_data['contact_id']

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        await contact_repository.delete_by_id(contact_id)
        await callback_query.answer(
            text='❗️ Контакт был успешно удален',
            show_alert=True,
        )
        contacts = await contact_repository.get_by_user_id(
            user_id=callback_query.from_user.id,
        )

    view = ContactListView(contacts)
    await edit_message_by_view(
        message=callback_query.message,
        view=view,
    )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_delete_contact,
        ContactDeleteCallbackData().filter(),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
