from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram.types import (
    Message,
    ChatType,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery, ContentType,
)

from common.repositories import HTTPClientFactory
from common.views import answer_view
from whisper.models import SecretMediaType
from whisper.repositories import ContactRepository, SecretMediaRepository
from whisper.services import (
    determine_media_file,
    get_message_method_by_media_type,
)
from whisper.states import SecretMediaCreateStates
from whisper.views import (
    SecretMediaCreateContactListView,
    SecretMediaCreateConfirmView, SecretMediaForShareView,
    SecretMediaCalledInGroupChatView,
)

__all__ = ('register_handlers',)


async def on_secret_media_command_called_in_group_chat(
        message: Message,
        bot: Bot,
) -> None:
    me = await bot.get_me()
    view = SecretMediaCalledInGroupChatView(me.username)
    await message.reply(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def on_secret_media_create_cancel(
        callback_query: CallbackQuery,
        state: FSMContext,

) -> None:
    await state.finish()
    await callback_query.answer('Отмена', show_alert=True)


async def on_secret_media_create_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        closing_http_client_factory: HTTPClientFactory,
        bot: Bot,
) -> None:
    state_data = await state.get_data()
    await state.finish()

    contact_id: int = state_data['contact_id']
    file_id: str = state_data['file_id']
    description: str | None = state_data['description']
    media_type_value: int = state_data['media_type_value']

    async with closing_http_client_factory() as http_client:
        secret_media_repository = SecretMediaRepository(http_client)
        secret_media = await secret_media_repository.create(
            contact_id=contact_id,
            file_id=file_id,
            description=description,
            media_type=media_type_value,
        )

    me = await bot.get_me()
    view = SecretMediaForShareView(
        bot_username=me.username,
        secret_media=secret_media,
    )
    sent_message = await answer_view(message=callback_query.message, view=view)
    await sent_message.reply('Вы можете переслать это сообщение получателю')


async def on_media_description_skip(
        callback_query: CallbackQuery,
        state: FSMContext,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    await SecretMediaCreateStates.confirm.set()
    await state.update_data(description=None)
    state_data = await state.get_data()

    contact_id: int = state_data['contact_id']
    file_id: str = state_data['file_id']
    media_type_value: int = state_data['media_type_value']
    media_type = SecretMediaType(media_type_value)

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contact = await contact_repository.get_by_id(contact_id)

    view = SecretMediaCreateConfirmView(
        contact=contact,
        media_type=media_type,
        description=None,
    )
    message_method = get_message_method_by_media_type(
        message=callback_query.message,
        media_type=media_type,
    )
    await message_method(file_id)
    await answer_view(message=callback_query.message, view=view)


async def on_media_description(
        message: Message,
        state: FSMContext,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    if len(message.text) > 64:
        await message.reply('❌ Описание не должно быть длиннее 64 символов')
        return
    await SecretMediaCreateStates.confirm.set()
    await state.update_data(description=message.text)
    state_data = await state.get_data()

    contact_id: int = state_data['contact_id']
    file_id: str = state_data['file_id']
    media_type_value: int = state_data['media_type_value']
    media_type = SecretMediaType(media_type_value)

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contact = await contact_repository.get_by_id(contact_id)

    view = SecretMediaCreateConfirmView(
        contact=contact,
        media_type=media_type,
        description=message.text,
    )
    message_method = get_message_method_by_media_type(
        message=message,
        media_type=media_type,
    )
    await message_method(file_id)
    await answer_view(message=message, view=view)


async def on_media_file(
        message: Message,
        state: FSMContext,
) -> None:
    file_id, media_type = determine_media_file(message)
    await state.update_data(file_id=file_id, media_type_value=media_type.value)
    await SecretMediaCreateStates.description.set()
    await message.answer(
        text='Вы можете ввести описание (оно будет показано получателю)',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Пропустить',
                        callback_data='skip',
                    )
                ],
            ],
        ),
    )


async def on_contact_choice(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    contact_id = int(callback_query.data)
    await state.update_data(contact_id=contact_id)
    await SecretMediaCreateStates.media.set()
    await callback_query.message.answer(
        'Отправьте ваше медиа, которое хотите секретно отправить.'
        ' Это может быть фото, видео, стикер, войс,'
        ' кружочек, документ, аудио или гифка',
    )


async def on_secret_media_command(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contacts = await contact_repository.get_by_user_id(message.from_user.id)
    not_hidden_contacts = [
        contact for contact in contacts
        if not contact.is_hidden
    ]
    view = SecretMediaCreateContactListView(not_hidden_contacts)
    await SecretMediaCreateStates.contact.set()
    await answer_view(message=message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_secret_media_create_cancel,
        Text('cancel'),
        chat_type=ChatType.PRIVATE,
        state=SecretMediaCreateStates.confirm,
    )
    dispatcher.register_callback_query_handler(
        on_secret_media_create_confirm,
        Text('confirm'),
        chat_type=ChatType.PRIVATE,
        state=SecretMediaCreateStates.confirm,
    )
    dispatcher.register_callback_query_handler(
        on_media_description_skip,
        Text('skip'),
        chat_type=ChatType.PRIVATE,
        state=SecretMediaCreateStates.description,
    )
    dispatcher.register_message_handler(
        on_media_description,
        content_types=ContentType.TEXT,
        chat_type=ChatType.PRIVATE,
        state=SecretMediaCreateStates.description,
    )
    dispatcher.register_message_handler(
        on_media_file,
        content_types=(
            ContentType.PHOTO,
            ContentType.VOICE,
            ContentType.AUDIO,
            ContentType.VIDEO,
            ContentType.VIDEO_NOTE,
            ContentType.DOCUMENT,
            ContentType.STICKER,
            ContentType.ANIMATION,
        ),
        chat_type=ChatType.PRIVATE,
        state=SecretMediaCreateStates.media,
    )
    dispatcher.register_callback_query_handler(
        on_contact_choice,
        chat_type=ChatType.PRIVATE,
        state=SecretMediaCreateStates.contact,
    )
    dispatcher.register_message_handler(
        on_secret_media_command_called_in_group_chat,
        Command('secret_media'),
        chat_type=(ChatType.GROUP, ChatType.SUPERGROUP),
        state='*',
    )
    dispatcher.register_message_handler(
        on_secret_media_command,
        Command('secret_media') | CommandStart(deep_link='secret_media'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
