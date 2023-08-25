from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import (
    TeamDetailCallbackData,
    TeamMemberDetailCallbackData,
    TeamMemberDeleteCallbackData,
    TeamMemberCreateCallbackData,
)
from models import TeamMember, TeamMemberStatus
from views.base import View

__all__ = (
    'TeamMemberListView',
    'TeamMemberDetailView',
)


def humanize_team_member_status(team_member_status: TeamMemberStatus) -> str:
    team_member_status_to_text = {
        TeamMemberStatus.MEMBER: 'участник',
        TeamMemberStatus.OWNER: 'создатель',
    }
    return team_member_status_to_text.get(
        team_member_status,
        team_member_status.name.lower(),
    )


class TeamMemberDetailView(View):

    def __init__(self, team_member: TeamMember,
                 current_team_member: TeamMember):
        self.__team_member = team_member
        self.__current_team_member = current_team_member

    def get_text(self) -> str:
        humanized_status = humanize_team_member_status(
            team_member_status=self.__team_member.status,
        )
        if self.__team_member == self.__current_team_member:
            return (
                f'Вы участник секретной группы: {self.__team_member.name}\n'
                f'Ваш статус: {humanized_status}'
            )
        return f'Участник секретной группы: {self.__team_member.name}'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        is_owner = self.__current_team_member.status == TeamMemberStatus.OWNER
        is_not_self = self.__team_member != self.__current_team_member
        if is_owner and is_not_self:
            markup.row(
                InlineKeyboardButton(
                    text='❌🗑️ Исключить из секретной группы',
                    callback_data=TeamMemberDeleteCallbackData().new(
                        team_member_id=self.__team_member.id,
                    ),
                ),
            )
        return markup


class TeamMemberListView(View):
    text = 'Участники секретной группы'

    def __init__(
            self,
            *,
            team_members: Iterable[TeamMember],
            team_id: int,
            current_user_id: int,
    ):
        self.__team_members = tuple(team_members)
        self.__team_id = team_id
        self.__current_user_id = current_user_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        for team_member in self.__team_members:
            name = team_member.user_username or team_member.user_fullname
            markup.row(
                InlineKeyboardButton(
                    text=name,
                    callback_data=TeamMemberDetailCallbackData().new(
                        team_member_id=team_member.id,
                    ),
                )
            )

        is_current_user_owner = any((
            team_member for team_member in self.__team_members
            if team_member.user_id == self.__current_user_id
               and team_member.status == TeamMemberStatus.OWNER
        ))
        has_members = bool(self.__team_members)
        can_add_members = is_current_user_owner and has_members

        if can_add_members:
            markup.row(
                InlineKeyboardButton(
                    text='➕ Добавить',
                    callback_data=TeamMemberCreateCallbackData().new(
                        team_id=self.__team_id,
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
