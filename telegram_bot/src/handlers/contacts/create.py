from aiogram import Router, F
from aiogram.filters import Command, invert_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models import User
from repositories import ContactRepository, UserRepository
from repositories import HTTPClientFactory
from services import (
    get_or_create_user,
    can_create_new_contact,
)
from states import ContactCreateWaitForForwardedMessage

__all__ = ('register_handlers',)


async def on_contact_create_via_forwarded_message(
        message: Message,
        user: User,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    name = message.forward_from.username or message.forward_from.full_name
    async with closing_http_client_factory() as http_client:
        contact = ContactRepository(http_client)
        contacts = await contact.get_by_user_id(user.id)
        if not can_create_new_contact(
            contacts_count=len(contacts),
            is_premium=user.is_premium,
        ):
            await message.reply(
                '🤭 Вы не можете иметь больше 5 контактов за раз.'
                '\nЧтобы убрать лимит,'
                ' вы можете преобрести премиум подписку за 50 сомов/месяц'
            )
            return

        await contact.create(
            of_user_id=user.id,
            to_user_id=message.forward_from.id,
            private_name=name,
            public_name=name,
        )
        await message.reply(
            '✅ Контакт успешно добавлен.'
            ' Вы можете продолжать пересылать сообщения'
            ' чтобы добавить кого-то в контакты'
        )


async def on_enable_contact_create_via_forwarded_message_mode(
        message: Message,
        state: FSMContext
) -> None:
    await state.set_state(ContactCreateWaitForForwardedMessage.enabled)
    await message.reply(
        'Чтобы добавить кого-то, перешлите сообщение сюда любое его сообщение'
    )


async def on_contact_command_is_not_replied_to_user(
        message: Message,
) -> None:
    await message.reply(
        'Вы должны <b><u>ответить</u></b> на сообщение другого пользователя\n'
        'Подробная инструкция: <a href="https://graph.org/Kak-dobavit'
        '-polzovatelya-v-kontakty-08-14">*ссылка*</a>'
    )


async def on_add_contact(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
        user: User,
) -> None:
    reply = message.reply_to_message
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

        contacts = await contact_repository.get_by_user_id(message.from_user.id)
        if not can_create_new_contact(
                contacts_count=len(contacts),
                is_premium=user.is_premium,
        ):
            await message.reply(
                '🤭 Вы не можете иметь больше 5 контактов за раз.'
                '\nЧтобы убрать лимит,'
                ' вы можете преобрести премиум подписку за 50 сомов/месяц'
            )
            return

        await contact_repository.create(
            of_user_id=user.id,
            to_user_id=to_user.id,
            private_name=name,
            public_name=name,
        )
        await message.reply('✅ Контакт успешно добавлен')


def register_handlers(router: Router) -> None:
    router.message.register(
        on_contact_command_is_not_replied_to_user,
        Command('contact'),
        invert_f(F.reply_to_message),
        StateFilter('*'),
    )
    router.message.register(
        on_add_contact,
        Command('contact'),
        F.reply_to_message,
        StateFilter('*'),
    )
