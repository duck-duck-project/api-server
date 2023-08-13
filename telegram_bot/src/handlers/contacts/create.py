from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, IsReplyFilter
from aiogram.types import Message

from exceptions import ContactAlreadyExistsError
from repositories import ContactRepository, UserRepository
from repositories import HTTPClientFactory
from services import (
    get_or_create_user,
    can_create_new_contact
)

__all__ = ('register_handlers',)


async def on_contact_command_is_not_replied_to_user(
        message: Message,
) -> None:
    await message.reply(
        'Вы должны <b><u>ответить</u></b> на сообщение другого пользователя'
    )


async def on_add_contact(
        message: Message,
        reply: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    if reply.from_user.is_bot:
        await message.reply('Вы не можете добавить бота в контакты')
        return

    if message.from_user.id == reply.from_user.id:
        await message.reply('Вы хотите добавить себя в свои же контакты? 🤭')
        return

    name = reply.from_user.username or reply.from_user.full_name

    async with closing_http_client_factory() as http_client:
        user_repository = UserRepository(http_client)
        contact_repository = ContactRepository(http_client)

        to_user, is_to_user_created = await get_or_create_user(
            user_repository=user_repository,
            user_id=reply.from_user.id,
            fullname=reply.from_user.full_name,
            username=reply.from_user.username,
        )

        if not to_user.can_be_added_to_contacts:
            await message.reply(
                '😔 Этот пользователь запретил добавлять себя в контакты',
            )
            return

        of_user, is_of_user_created = await get_or_create_user(
            user_repository=user_repository,
            user_id=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
        )

        contacts = await contact_repository.get_by_user_id(message.from_user.id)
        if not can_create_new_contact(
                contacts_count=len(contacts),
                is_premium=of_user.is_premium,
        ):
            await message.reply(
                '🤭 Вы не можете иметь больше 5 контактов за раз.'
                '\nЧтобы убрать лимит,'
                ' вы можете преобрести премиум подписку за 30 сомов/месяц'
            )
            return

        try:
            await contact_repository.create(
                of_user_id=of_user.id,
                to_user_id=to_user.id,
                private_name=name,
                public_name=name,
            )
        except ContactAlreadyExistsError:
            await message.reply(
                '😶 Этот пользователь уже есть в ваших контактах',
            )
        else:
            await message.reply('✅ Контакт успешно добавлен')


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_contact_command_is_not_replied_to_user,
        Command('contact'),
        IsReplyFilter(is_reply=False),
        state='*',
    )
    dispatcher.register_message_handler(
        on_add_contact,
        Command('contact'),
        IsReplyFilter(is_reply=True),
        state='*',
    )
