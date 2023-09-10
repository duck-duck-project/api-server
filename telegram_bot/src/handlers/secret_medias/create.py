from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from models import SecretMediaType
from repositories import (
    ContactRepository,
    SecretMediaRepository,
)
from repositories import HTTPClientFactory
from services import (
    determine_media_file,
    get_message_method_by_media_type, send_view_to_user, filter_not_hidden,
)
from states import SecretMediaCreateStates
from views import (
    SecretMediaCreateContactListView,
    SecretMediaCreateConfirmView,
    SecretMediaForShareView,
    SecretMediaCalledInGroupChatView,
)
from views import answer_view

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
    await state.clear()
    await callback_query.answer('Отмена', show_alert=True)


async def on_secret_media_create_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot,
        secret_media_repository: SecretMediaRepository,
        contact_repository: ContactRepository,
) -> None:
    state_data = await state.get_data()
    await state.clear()

    contact_id: int = state_data['contact_id']
    file_id: str = state_data['file_id']
    description: str | None = state_data['description']
    media_type_value: int = state_data['media_type_value']

    secret_media = await secret_media_repository.create(
        contact_id=contact_id,
        file_id=file_id,
        description=description,
        media_type=media_type_value,
    )
    contact = await contact_repository.get_by_id(contact_id)

    me = await bot.get_me()

    view = SecretMediaForShareView(
        bot_username=me.username,
        secret_media=secret_media,
        from_user_username=contact.of_user.username or contact.of_user.fullname,
    )
    sent_message = await answer_view(message=callback_query.message, view=view)
    await sent_message.reply('Вы можете переслать это сообщение получателю')

    if contact.to_user.can_receive_notifications:
        await send_view_to_user(
            bot=bot,
            view=view,
            to_chat_id=contact.to_user.id,
            from_chat_id=contact.of_user.id,
        )


async def on_media_description_skip(
        callback_query: CallbackQuery,
        state: FSMContext,
        contact_repository: ContactRepository,
) -> None:
    await state.set_state(SecretMediaCreateStates.confirm)
    await state.update_data(description=None)
    state_data = await state.get_data()

    contact_id: int = state_data['contact_id']
    file_id: str = state_data['file_id']
    media_type_value: int = state_data['media_type_value']
    media_type = SecretMediaType(media_type_value)

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
        contact_repository: ContactRepository,
) -> None:
    if len(message.text) > 64:
        await message.reply('❌ Описание не должно быть длиннее 64 символов')
        return
    await state.set_state(SecretMediaCreateStates.confirm)
    await state.update_data(description=message.text)
    state_data = await state.get_data()

    contact_id: int = state_data['contact_id']
    file_id: str = state_data['file_id']
    media_type_value: int = state_data['media_type_value']
    media_type = SecretMediaType(media_type_value)

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
    await state.set_state(SecretMediaCreateStates.description)
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
    await state.set_state(SecretMediaCreateStates.media)
    await callback_query.message.edit_text(
        'Отправьте ваше медиа, которое хотите секретно отправить.'
        ' Это может быть фото, видео, стикер, войс,'
        ' кружочек, документ, аудио или гифка',
    )


async def on_secret_media_command(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
        state: FSMContext,
) -> None:
    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        contacts = await contact_repository.get_by_user_id(message.from_user.id)
    contacts = filter_not_hidden(contacts)
    view = SecretMediaCreateContactListView(contacts)
    await state.set_state(SecretMediaCreateStates.contact)
    await answer_view(message=message, view=view)


def register_handlers(router: Router) -> None:
    router.message.register(
        on_secret_media_command_called_in_group_chat,
        F.text.startswith('/secret_media'),
        F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
        StateFilter('*'),
    )
    router.message.register(
        on_secret_media_command,
        or_f(
            F.text.startswith('/secret_media'),
            F.text == '🖼️ Секретное медиа',
        ),
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
    router.callback_query.register(
        on_secret_media_create_cancel,
        F.data == 'cancel',
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter(SecretMediaCreateStates.confirm),
    )
    router.callback_query.register(
        on_secret_media_create_confirm,
        F.data == 'confirm',
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter(SecretMediaCreateStates.confirm),
    )
    router.callback_query.register(
        on_media_description_skip,
        F.data == 'skip',
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter(SecretMediaCreateStates.description),
    )
    router.message.register(
        on_media_description,
        F.text,
        F.chat.type == ChatType.PRIVATE,
        StateFilter(SecretMediaCreateStates.description),
    )
    router.message.register(
        on_media_file,
        or_f(
            F.photo,
            F.video,
            F.animation,
            F.voice,
            F.audio,
            F.document,
            F.sticker,
            F.video_note,
        ),
        F.chat.type == ChatType.PRIVATE,
        StateFilter(SecretMediaCreateStates.media),
    )
    router.callback_query.register(
        on_contact_choice,
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter(SecretMediaCreateStates.contact),
    )
