from celery import shared_task
from fast_depends import Depends, inject

from telegram.dependencies import get_telegram_bot_context
from telegram.services import TelegramBotContext
from users.selectors.users import iter_users_with_birthdays
from users.services.birthdays import is_beautiful_number

__all__ = ('send_beautiful_lifetime_date_notifications',)


@shared_task
@inject
def send_beautiful_lifetime_date_notifications(
        telegram_bot_context: TelegramBotContext = Depends(
            get_telegram_bot_context,
        ),
) -> None:
    for users in iter_users_with_birthdays():

        for user in users:

            if not is_beautiful_number(user.lifetime_in_days):
                continue

            text = (
                '🎉 Поздравляем!\n'
                f'🔥 Вы прожили {user.lifetime_in_days} дней на Земле!'
            )
            telegram_bot_context.send_if_not_blocked(user=user, text=text)
