from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import TeamDetailCallbackData
from models import TeamIdAndName
from views.base import View

__all__ = (
    'TeamListView',
)


class TeamListView(View):

    def __init__(self, teams: Iterable[TeamIdAndName]):
        self.__teams = tuple(teams)

    def get_text(self) -> str:
        return (
            'Список ваших секретных групп'
            if self.__teams
            else 'У вас нет ни одной секретной группе'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for team in self.__teams:
            markup.row(
                InlineKeyboardButton(
                    text=team.name,
                    callback_data=TeamDetailCallbackData().new(
                        team_id=team.id,
                    ),
                )
            )
        markup.row(
            InlineKeyboardButton(
                text='➕ Создать новую секретную группу',
                callback_data='create-team',
            )
        )
        return markup
