from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message

from callback_data import ContactUpdateCallbackData
from repositories import ContactRepository
from repositories import HTTPClientFactory
from views import edit_message_by_view
from views.contacts import ContactDetailView

__all__ = ('register_handlers',)


async def on_toggle_is_hidden_status_command(
        message: Message,
        contact_repository: ContactRepository,
) -> None:
    reply = message.reply_to_message
    is_hidden = message.text.startswith('/hide')

    contacts = await contact_repository.get_by_user_id(message.from_user.id)

    contact_to_update = None
    for contact in contacts:
        if contact.to_user.id == reply.from_user.id:
            contact_to_update = contact
            break

    if contact_to_update is None:
        await message.reply(
            f'❌ {reply.from_user.full_name} не ваш контакт')
        return

    await contact_repository.update(
        contact_id=contact_to_update.id,
        public_name=contact_to_update.public_name,
        private_name=contact.private_name,
        is_hidden=is_hidden,
    )
    text = '🙈 Контакт скрыт' if is_hidden else '🙉 Контакт больше не скрыт'
    await message.reply(text)


async def on_toggle_is_hidden_status(
        callback_query: CallbackQuery,
        callback_data: ContactUpdateCallbackData,
        closing_http_client_factory: HTTPClientFactory,
) -> None:

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contact = await contact_repository.get_by_id(callback_data.contact_id)
        await contact_repository.update(
            contact_id=callback_data.contact_id,
            public_name=contact.public_name,
            private_name=contact.private_name,
            is_hidden=not contact.is_hidden,
        )
        contact = await contact_repository.get_by_id(callback_data.contact_id)

    view = ContactDetailView(contact)
    await edit_message_by_view(message=callback_query.message, view=view)
    await callback_query.answer('✅ Статус скрытости обновлен')


def register_handlers(router: Router) -> None:
    router.message.register(
        on_toggle_is_hidden_status_command,
        Command('hide', 'show'),
        F.reply_to_message,
        StateFilter('*'),
    )
    router.callback_query.register(
        on_toggle_is_hidden_status,
        ContactUpdateCallbackData.filter(F.field == 'is_hidden'),
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
