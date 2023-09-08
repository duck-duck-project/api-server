from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from repositories import ContactRepository
from views import render_message_or_callback_query
from views.contacts import ContactListView

__all__ = ('register_handlers',)


async def on_show_contacts_list(
        message_or_callback_query: Message | CallbackQuery,
        contact_repository: ContactRepository,
) -> None:
    user_id = message_or_callback_query.from_user.id
    contacts = await contact_repository.get_by_user_id(user_id)
    view = ContactListView(contacts)
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=view,
    )


def register_handlers(router: Router) -> None:
    router.message.register(
        on_show_contacts_list,
        F.text == '👥 Контакты',
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
    router.callback_query.register(
        on_show_contacts_list,
        F.data == 'show-contacts-list',
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
