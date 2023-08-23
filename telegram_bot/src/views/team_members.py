from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import TeamDetailCallbackData, TeamMemberDetailCallbackData
from views.base import View

__all__ = ('TeamMemberListView',)


class TeamMemberListView(View):
    text = 'Участники секретной группы'

    def __init__(self, *, team_members: Iterable, team_id: int):
        self.__team_members = tuple(team_members)
        self.__team_id = team_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        for team_member in self.__team_members:
            markup.row(
                InlineKeyboardButton(
                    text='участник',
                    callback_data=TeamMemberDetailCallbackData().new(
                        team_member_id=team_member.id,
                    ),
                )
            )

        markup.row(
            InlineKeyboardButton(
                text='🔙 Назад',
                callback_data=TeamDetailCallbackData().new(
                    team_id=self.__team_id,
                )
            )
        )
        return markup
