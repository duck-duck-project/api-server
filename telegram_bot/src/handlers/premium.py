from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, Update, CallbackQuery

from exceptions import UserHasNoPremiumSubscriptionError
from views import (
    PremiumSubscriptionInfoView,
    render_message_or_callback_query
)

__all__ = ('register_handlers',)


async def on_user_has_no_premium_subscription_error(
        update: Update,
        exception: UserHasNoPremiumSubscriptionError,
) -> bool:
    text = str(exception)
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    return True


async def on_show_premium_subscription_info(
        message_or_callback_query: Message | CallbackQuery,
) -> None:
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=PremiumSubscriptionInfoView(),
        disable_web_page_preview=True,
    )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_user_has_no_premium_subscription_error,
        exception=UserHasNoPremiumSubscriptionError,
    )
    dispatcher.register_message_handler(
        on_show_premium_subscription_info,
        Command('premium'),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        on_show_premium_subscription_info,
        Text('show-premium-subscription'),
        state='*',
    )
