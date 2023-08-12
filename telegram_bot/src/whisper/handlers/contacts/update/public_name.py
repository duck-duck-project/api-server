from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType

from common.repositories import HTTPClientFactory
from common.views import answer_view
from whisper.callback_data import ContactUpdateCallbackData
from whisper.repositories import ContactRepository
from whisper.states import ContactUpdateStates
from whisper.views import ContactDetailView

__all__ = ('register_handlers',)


async def on_start_contact_public_name_update_flow(
        callback_query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
) -> None:
    contact_id: int = callback_data['contact_id']
    await ContactUpdateStates.public_name.set()
    await state.update_data(contact_id=contact_id)
    await callback_query.message.reply(
        '👀 Введите новое публичное имя контакта'
    )


async def on_contact_new_public_name_input(
        message: Message,
        state: FSMContext,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    state_data = await state.get_data()
    await state.finish()
    contact_id: int = state_data['contact_id']

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contact = await contact_repository.get_by_id(contact_id)
        await contact_repository.update(
            contact_id=contact_id,
            private_name=contact.private_name,
            public_name=message.text,
        )
        contact = await contact_repository.get_by_id(contact_id)

    await message.reply('✅ Публичное имя контакта обновлено')
    view = ContactDetailView(contact)
    await answer_view(message=message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_contact_new_public_name_input,
        chat_type=ChatType.PRIVATE,
        state=ContactUpdateStates.public_name,
    )
    dispatcher.register_callback_query_handler(
        on_start_contact_public_name_update_flow,
        ContactUpdateCallbackData().filter(field='public_name'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
