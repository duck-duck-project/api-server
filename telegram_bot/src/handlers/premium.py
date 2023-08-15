from aiogram import Dispatcher

__all__ = ('register_handlers',)

from aiogram.dispatcher.filters import Command

from aiogram.types import Message

from views import answer_view, PremiumSubscriptionInfoView


async def on_show_premium_subscription_info(
        message: Message,
) -> None:
    await answer_view(
        message=message,
        view=PremiumSubscriptionInfoView(),
        disable_web_page_preview=True,
    )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_premium_subscription_info,
        Command('premium'),
        state='*',
    )
