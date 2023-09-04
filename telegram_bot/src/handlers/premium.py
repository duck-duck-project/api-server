from aiogram import F, Router
from aiogram.filters import Command, ExceptionTypeFilter, StateFilter
from aiogram.types import Message, Update, CallbackQuery

from exceptions import UserHasNoPremiumSubscriptionError
from views import (
    PremiumSubscriptionInfoView,
    render_message_or_callback_query,
    PremiumSubscriptionLinkView,
)

__all__ = ('router',)

router = Router(name=__name__)


async def on_user_has_no_premium_subscription_error(
        update: Update,
        exception: UserHasNoPremiumSubscriptionError,
) -> bool:
    text = str(exception)
    view = PremiumSubscriptionLinkView(text)
    await render_message_or_callback_query(
        message_or_callback_query=update.message or update.callback_query,
        view=view,
        disable_web_page_preview=True,
    )
    return True


async def on_show_premium_subscription_info(
        message_or_callback_query: Message | CallbackQuery,
) -> None:
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=PremiumSubscriptionInfoView(),
        disable_web_page_preview=True,
    )


router.errors.register(
    on_user_has_no_premium_subscription_error,
    ExceptionTypeFilter(UserHasNoPremiumSubscriptionError),
)
router.message.register(
    on_show_premium_subscription_info,
    Command('premium'),
    StateFilter('*'),
)
router.callback_query.register(
    on_show_premium_subscription_info,
    F.data == 'show-premium-subscription',
    StateFilter('*'),
)
