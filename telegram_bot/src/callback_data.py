from uuid import UUID

from aiogram.filters.callback_data import CallbackData

__all__ = (
    'InvertedSecretMessageDetailCallbackData',
    'SecretMessageDetailCallbackData',
    'ContactDetailCallbackData',
    'ContactUpdateCallbackData',
    'ContactDeleteCallbackData',
    'UserUpdateCallbackData',
    'TeamDetailCallbackData',
    'TeamUpdateCallbackData',
    'TeamDeleteAskForConfirmationCallbackData',
    'TeamMemberDetailCallbackData',
    'TeamMemberDeleteCallbackData',
    'SecretMessageForTeamCallbackData',
    'TeamMemberListCallbackData',
    'TeamMemberCreateCallbackData',
    'TeamMemberCreateAcceptInvitationCallbackData',
)


class UserUpdateCallbackData(CallbackData, prefix='user-update'):
    field: str


class InvertedSecretMessageDetailCallbackData(
    CallbackData,
    prefix='inverted-whisp',
):
    contact_id: int
    secret_message_id: UUID


class SecretMessageDetailCallbackData(CallbackData, prefix='show-whisp'):
    contact_id: int
    secret_message_id: UUID


class ContactDetailCallbackData(CallbackData, prefix='contact-detail'):
    contact_id: int


class ContactUpdateCallbackData(CallbackData, prefix='contact-update'):
    contact_id: int
    field: str


class ContactDeleteCallbackData(CallbackData, prefix='contact-delete'):
    contact_id: int


class TeamDetailCallbackData(CallbackData, prefix='team-detail'):
    team_id: int


class TeamUpdateCallbackData(CallbackData, prefix='team-update'):
    team_id: int


class TeamDeleteAskForConfirmationCallbackData(
    CallbackData,
    prefix='team-delete-ask-for-confirmation',
):
    team_id: int


class TeamMemberDetailCallbackData(CallbackData, prefix='team-member-detail'):
    team_member_id: int


class TeamMemberDeleteCallbackData(CallbackData, prefix='team-member-delete'):
    team_member_id: int


class SecretMessageForTeamCallbackData(
    CallbackData,
    prefix='secret-message-team',
):
    team_id: int
    secret_message_id: UUID


class TeamMemberListCallbackData(CallbackData, prefix='team-member-list'):
    team_id: int


class TeamMemberCreateCallbackData(CallbackData, prefix='team-member-create'):
    team_id: int


class TeamMemberCreateAcceptInvitationCallbackData(
    CallbackData,
    prefix='team-member-create-accept-invitation',
):
    team_id: int
