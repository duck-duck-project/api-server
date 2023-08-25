from uuid import UUID

from aiogram.utils.callback_data import CallbackData

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
)


class UserUpdateCallbackData(CallbackData):

    def __init__(self):
        super().__init__('user-update', 'field')


class ParseContactIdMixin:

    def parse(self, callback_data: str) -> dict:
        callback_data = super().parse(callback_data)
        return callback_data | {
            'contact_id': int(callback_data['contact_id']),
        }


class ParseSecretMessageIdMixin:

    def parse(self, callback_data: str) -> dict:
        callback_data = super().parse(callback_data)
        return callback_data | {
            'secret_message_id': UUID(callback_data['secret_message_id']),
        }


class InvertedSecretMessageDetailCallbackData(
    CallbackData,
    ParseContactIdMixin,
):

    def __init__(self):
        super().__init__(
            'show-inverted-whisp',
            'contact_id',
            'secret_message_id',
        )


class SecretMessageDetailCallbackData(
    ParseContactIdMixin,
    ParseSecretMessageIdMixin,
    CallbackData,
):

    def __init__(self):
        super().__init__('show-whisp', 'contact_id', 'secret_message_id')


class ContactDetailCallbackData(CallbackData, ParseContactIdMixin):

    def __init__(self):
        super().__init__('contact-detail', 'contact_id')


class ContactUpdateCallbackData(CallbackData, ParseContactIdMixin):

    def __init__(self):
        super().__init__('contact-update', 'contact_id', 'field')


class ContactDeleteCallbackData(CallbackData, ParseContactIdMixin):

    def __init__(self):
        super().__init__('contact-delete', 'contact_id')


class ParseTeamIdMixin:

    def parse(self, callback_data: str) -> dict:
        callback_data = super().parse(callback_data)
        return callback_data | {'team_id': int(callback_data['team_id'])}


class TeamDetailCallbackData(CallbackData, ParseTeamIdMixin):

    def __init__(self):
        super().__init__('team-detail', 'team_id')


class TeamUpdateCallbackData(CallbackData, ParseTeamIdMixin):

    def __init__(self):
        super().__init__('team-update', 'team_id', 'field')


class TeamDeleteAskForConfirmationCallbackData(CallbackData, ParseTeamIdMixin):

    def __init__(self):
        super().__init__('team-delete-ask-for-confirmation', 'team_id')


class ParseTeamMemberIdMixin:

    def parse(self, callback_data: str) -> dict:
        callback_data = super().parse(callback_data)
        return callback_data | {
            'team_member_id': int(callback_data['team_member_id']),
        }


class TeamMemberDetailCallbackData(CallbackData, ParseTeamMemberIdMixin):

    def __init__(self):
        super().__init__('team-member-detail', 'team_member_id')


class TeamMemberDeleteCallbackData(CallbackData, ParseTeamMemberIdMixin):

    def __init__(self):
        super().__init__('team-member-delete', 'team_member_id')


class SecretMessageForTeamCallbackData(
    ParseTeamIdMixin,
    ParseSecretMessageIdMixin,
    CallbackData,
):

    def __init__(self):
        super().__init__('secret-message-team', 'team_id', 'secret_message_id')


class TeamMemberListCallbackData(ParseTeamIdMixin, CallbackData):

    def __init__(self):
        super().__init__('team-member-list', 'team_id')


class TeamMemberCreateCallbackData(ParseTeamIdMixin, CallbackData):

    def __init__(self):
        super().__init__('team-member-create', 'team_id')
