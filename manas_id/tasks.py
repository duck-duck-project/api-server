import contextlib

from celery import shared_task
from django.utils import timezone
from fast_depends import Depends, inject

from economics.services.allowance import create_stipend
from manas_id.selectors import iter_manas_ids
from telegram.dependencies import get_telegram_bot_service
from telegram.services import TelegramBotService


@shared_task
def give_away_stipends(
) -> None:
    for manas_ids in iter_manas_ids():
        
        


@shared_task
@inject
def congratulate_users_with_birthday(
        telegram_bot_service: TelegramBotService = Depends(
            get_telegram_bot_service,
        ),
) -> None:
    now = timezone.now() + timezone.timedelta(hours=6)

    for manas_ids in iter_manas_ids():
        for manas_id in manas_ids:
            if manas_id.born_at.day == now.day and manas_id.born_at.month == now.month:
                age = now.year - manas_id.born_at.year
                if age % 100 in (11, 12, 13, 14):
                    suffix = 'лет'
                elif age % 10 == 1:
                    suffix = 'год'
                elif age % 10 in (2, 3, 4):
                    suffix = 'года'
                else:
                    suffix = 'лет'
                text = (
                    f'❗️ Сегодня {manas_id.first_name} исполняется {age} {suffix}!\n'
                    f'🎉 Поздравляем'
                )
                telegram_bot_service.send_message(
                    chat_id='@studmanas',
                    text=text,
                )
@shared_task
def give_awaya_presents(
) -> None:
    now = timezone.now() 

for manas_ids in  iter_manas_ids():
    for manas_id in manas_ids:
            with contextlib.suppress(Exception):
                create_presents(user=manas_id.user)
