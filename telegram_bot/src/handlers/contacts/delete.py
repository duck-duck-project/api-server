from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import ContactDeleteCallbackData
from repositories import ContactRepository
from views import edit_message_by_view
from views.contacts import ContactListView

__all__ = ('register_handlers',)


async def on_delete_contact(
        callback_query: CallbackQuery,
        callback_data: ContactDeleteCallbackData,
        contact_repository: ContactRepository,
) -> None:
    await contact_repository.delete_by_id(callback_data.contact_id)
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


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_delete_contact,
        ContactDeleteCallbackData.filter(),
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
