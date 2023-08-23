from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import (
    TeamDetailCallbackData,
    TeamDeleteAskForConfirmationCallbackData,
    TeamUpdateCallbackData,
)
from models import TeamIdAndName
from views.base import View

__all__ = (
    'TeamDetailView',
    'TeamListView',
    'TeamDeleteAskForConfirmationView',
)


class TeamDetailView(View):

    def __init__(self, team):
        self.__team = team

    def get_text(self) -> str:
        return

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='👥 Участники',
                        callback_data='',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='📝 Переименовать секретную группу',
                        callback_data=TeamUpdateCallbackData().new(
                            team_id=self.__team.id,
                            field='name',
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='❌🗑️ Удалить секретную группу',
                        callback_data=(
                            TeamDeleteAskForConfirmationCallbackData().new(
                                team_id=self.__team.id,
                            )
                        ),
                    ),
                ]
            ],
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


class TeamDeleteAskForConfirmationView(View):
    text = 'Вы уверены, что хотите удалить секретную группу?'

    def __init__(self, team_id: int):
        self.__team_id = team_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='🔥 Удалить',
                        callback_data='confirm'
                    ),
                    InlineKeyboardButton(
                        text='♻️ Отменить',
                        callback_data=TeamDetailCallbackData().new(
                            team_id=self.__team_id,
                        )
                    )
                ],
            ],
        )
