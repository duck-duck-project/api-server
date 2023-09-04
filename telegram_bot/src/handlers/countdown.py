from zoneinfo import ZoneInfo

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from services import (
    get_time_before_studies_start,
    calculate_urgency_coefficient,
)
from views import answer_view
from views.countdown import TimeBeforeStudiesStartCountdownView

__all__ = ('router',)

router = Router(name=__name__)


async def on_show_time_before_studies_start(
        message: Message,
        timezone: ZoneInfo,
) -> None:
    time_before_studies_start = get_time_before_studies_start(timezone)
    urgency_coefficient = calculate_urgency_coefficient(
        days_left=time_before_studies_start.days,
    )
    view = TimeBeforeStudiesStartCountdownView(
        time_before_studies_start=time_before_studies_start,
        urgency_coefficient=urgency_coefficient,
    )
    await answer_view(message=message, view=view)


router.message.register(
    on_show_time_before_studies_start,
    Command('time'),
    StateFilter('*'),
)
