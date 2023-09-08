from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import ContactDetailCallbackData
from repositories import ContactRepository
from repositories import HTTPClientFactory
from views import edit_message_by_view
from views.contacts import ContactDetailView

__all__ = ('register_handlers',)


async def on_show_contact_detail(
        callback_query: CallbackQuery,
        callback_data: ContactDetailCallbackData,
        contact_repository: ContactRepository,
) -> None:
    contact = await contact_repository.get_by_id(callback_data.contact_id)
    view = ContactDetailView(contact)
    await edit_message_by_view(
        message=callback_query.message,
        view=view,
    )


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_show_contact_detail,
        ContactDetailCallbackData.filter(),
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
