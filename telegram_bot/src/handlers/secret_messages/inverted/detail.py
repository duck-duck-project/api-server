from uuid import UUID

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import InvertedSecretMessageDetailCallbackData
from repositories import (
    HTTPClientFactory,
    ContactRepository,
    SecretMessageRepository,
)

__all__ = ('register_handlers',)


async def on_show_inverted_message(
        callback_query: CallbackQuery,
        callback_data: InvertedSecretMessageDetailCallbackData,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
        secret_message_repository = SecretMessageRepository(http_client)

        contact = await contact_repository.get_by_id(
            contact_id=callback_data.contact_id,
        )
        secret_message = await secret_message_repository.get_by_id(
            secret_message_id=callback_data.secret_message_id,
        )

    if callback_query.from_user.id == contact.to_user.id:
        text = 'Это сообщение не предназначено для тебя 😉'
    else:
        text = secret_message.text
    await callback_query.answer(text, show_alert=True)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_show_inverted_message,
        InvertedSecretMessageDetailCallbackData.filter(),
        StateFilter('*'),
    )
