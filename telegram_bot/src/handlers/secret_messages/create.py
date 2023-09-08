from uuid import UUID

from aiogram import Bot, Router, F
from aiogram.filters import StateFilter, invert_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ChosenInlineResult, InlineQuery

from filters import secret_message_valid_format_chosen_inline_result_filter
from repositories import (
    SecretMessageRepository,
    ContactRepository
)
from services import send_view_to_user
from views import (
    answer_view,
    SecretMessagePromptView,
    SecretMessageTextMissingInlineQueryView, SecretMessageNotificationView,
)

__all__ = ('register_handlers',)


async def on_show_inline_query_prompt(message: Message) -> None:
    await answer_view(message=message, view=SecretMessagePromptView())


async def on_secret_message_text_missing(inline_query: InlineQuery) -> None:
    items = [
        SecretMessageTextMissingInlineQueryView()
        .get_inline_query_result_article()
    ]
    await inline_query.answer(items, cache_time=1)


async def on_message_created(
        chosen_inline_result: ChosenInlineResult,
        state: FSMContext,
        secret_message_repository: SecretMessageRepository,
        contact_repository: ContactRepository,
        bot: Bot,
        contact_id: int,
        is_contact: bool,
):
    state_data = await state.get_data()
    secret_message_id = UUID(state_data['secret_message_id'])
    is_inverted = chosen_inline_result.query.startswith('!')
    text: str = chosen_inline_result.query.lstrip('!')

    if not (0 < len(text) <= 200):
        return

    await secret_message_repository.create(
        secret_message_id=secret_message_id,
        text=text,
    )

    if is_contact:
        contact = await contact_repository.get_by_id(contact_id)
        if contact.to_user.can_receive_notifications and not is_inverted:
            view = SecretMessageNotificationView(
                secret_message_id=secret_message_id,
                contact=contact,
            )
            await send_view_to_user(
                bot=bot,
                view=view,
                to_chat_id=contact.to_user.id,
                from_chat_id=contact.of_user.id,
            )


def register_handlers(router: Router) -> None:
    router.chosen_inline_result.register(
        on_message_created,
        secret_message_valid_format_chosen_inline_result_filter,
        StateFilter('*'),
    )
    router.inline_query.register(
        on_secret_message_text_missing,
        invert_f(F.query),
        StateFilter('*'),
    )
    router.message.register(
        on_show_inline_query_prompt,
        or_f(
            F.text.startswith('/secret_message'),
            F.text == '📩 Секретное сообщение',
        ),
        StateFilter('*'),
    )
