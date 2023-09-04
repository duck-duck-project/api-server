from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    TeamDetailCallbackData,
    TeamMemberDetailCallbackData,
    TeamMemberCreateCallbackData,
    TeamMemberCreateAcceptInvitationCallbackData,
)
from callback_data import (
    TeamMemberListCallbackData,
    TeamMemberDeleteCallbackData,
)
from models import TeamMember
from models import (
    TeamMemberStatus,
    Contact,
    User,
    Team,
)
from views.base import View

__all__ = (
    'TeamMemberListView',
    'TeamMemberDetailView',
    'TeamMemberCreateChooseContactView',
    'TeamMemberCreateAcceptInvitationCallbackData',
    'TeamMemberCreateAskForConfirmationView',
    'TeamMemberMenuDetailView',
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
        keyboard = InlineKeyboardBuilder()

        for team_member in self.__team_members:
            name = team_member.user_username or team_member.user_fullname
            keyboard.row(
                InlineKeyboardButton(
                    text=name,
                    callback_data=TeamMemberDetailCallbackData(
                        team_member_id=team_member.id,
                    ).pack(),
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
            keyboard.row(
                InlineKeyboardButton(
                    text='➕ Добавить',
                    callback_data=TeamMemberCreateCallbackData(
                        team_id=self.__team_id,
                    ).pack(),
                )
            )

        keyboard.row(
            InlineKeyboardButton(
                text='🔙 Назад',
                callback_data=TeamDetailCallbackData(
                    team_id=self.__team_id,
                ).pack()
            )
        )
        return keyboard.as_markup()


class TeamMemberCreateChooseContactView(View):

    def __init__(self, *, contacts: Iterable[Contact], team_id: int):
        self.__contacts = tuple(contacts)
        self.__team_id = team_id

    def get_text(self) -> str:
        return (
            'Выберите контакт, которого хотите добавить в секретную группу 😄'
            if self.__contacts else
            'У вас нет контактов, которых можно добавить в секретную группу 😔'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for contact in self.__contacts:
            keyboard.row(
                InlineKeyboardButton(
                    text=contact.private_name,
                    callback_data=str(contact.id),
                ),
            )

        keyboard.row(
            InlineKeyboardButton(
                text='🔙 Назад',
                callback_data=TeamDetailCallbackData(
                    team_id=self.__team_id,
                ).pack(),
            ),
        )
        return keyboard.as_markup()


class TeamMemberCreateAskForConfirmationView(View):

    def __init__(self, *, from_user: User, team: Team):
        self.__from_user = from_user
        self.__team = team

    def get_text(self) -> str:
        from_user_name = self.__from_user.username or self.__from_user.fullname
        return (
            f'❗️ <b>{from_user_name}</b> предложил(-а) вам вступить в'
            f' секретный чат <b>{self.__team.name}</b>'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='✅ Вступить',
                        callback_data=(
                            TeamMemberCreateAcceptInvitationCallbackData(
                                team_id=self.__team.id,
                            ).pack()
                        ),
                    ),
                ],
            ],
        )


class TeamMemberMenuDetailView(View):

    def __init__(self, team_member: TeamMember):
        self.__team_member = team_member

    def get_text(self) -> str:
        humanized_status = humanize_team_member_status(
            team_member_status=self.__team_member.status,
        )
        name = (
                self.__team_member.user_username
                or self.__team_member.user_fullname
        )
        return (
            f'👤 Имя: {name}\n'
            f'🌟 Статус: {humanized_status}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='❌ Удалить',
                        callback_data=TeamMemberDeleteCallbackData(
                            team_member_id=self.__team_member.id,
                        ).pack(),
                    ),
                ],
            ],
        )
