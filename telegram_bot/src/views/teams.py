from collections.abc import Iterable
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    TeamDetailCallbackData,
    TeamDeleteAskForConfirmationCallbackData,
    TeamMemberListCallbackData,
)
from models import TeamIdAndName, Team
from views.base import View

__all__ = (
    'TeamCreateAskForNameView',
    'TeamDetailView',
    'TeamListView',
    'TeamDeleteAskForConfirmationView',
)


class TeamCreateAskForNameView(View):
    text = '📝 Введите название секретной группы'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='show-teams-list',
                ),
            ],
        ],
    )


class TeamDetailView(View):

    def __init__(self, team: Team, timezone: ZoneInfo):
        self.__team = team
        self.__timezone = timezone

    def get_text(self) -> str:
        created_at_local = self.__team.created_at.astimezone(self.__timezone)
        return (
            f'Секретная группа: {self.__team.name}\n'
            f'Количество участников: {self.__team.members_count}\n'
            f'Дата создания: {created_at_local:%H:%M %d.%m.%Y}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='👥 Участники',
                        callback_data=TeamMemberListCallbackData(
                            team_id=self.__team.id,
                        ).pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='❌🗑️ Удалить секретную группу',
                        callback_data=(
                            TeamDeleteAskForConfirmationCallbackData(
                                team_id=self.__team.id,
                            ).pack()
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
            else 'У вас нет ни одной секретной группы'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        for team in self.__teams:
            keyboard.row(
                InlineKeyboardButton(
                    text=team.name,
                    callback_data=TeamDetailCallbackData(
                        team_id=team.id,
                    ).pack(),
                )
            )
        keyboard.row(
            InlineKeyboardButton(
                text='➕ Создать новую секретную группу',
                callback_data='create-team',
            )
        )
        return keyboard.as_markup()


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
                        callback_data=TeamDetailCallbackData(
                            team_id=self.__team_id,
                        ).pack()
                    )
                ],
            ],
        )
