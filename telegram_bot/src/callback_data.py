from uuid import UUID

from aiogram.utils.callback_data import CallbackData

__all__ = (
    'InvertedSecretMessageDetailCallbackData',
    'SecretMessageDetailCallbackData',
    'ContactDetailCallbackData',
    'ContactUpdateCallbackData',
    'ContactDeleteCallbackData',
)


class ParseContactIdMixin:

    def parse(self, callback_data: str) -> dict:
        callback_data = super().parse(callback_data)
        return callback_data | {
            'contact_id': int(callback_data['contact_id']),
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


class SecretMessageDetailCallbackData(CallbackData, ParseContactIdMixin):

    def __init__(self):
        super().__init__('show-whisp', 'contact_id', 'secret_message_id')

    def parse(self, callback_data: str) -> dict:
        callback_data = super().parse(callback_data)
        return callback_data | {
            'secret_message_id': UUID(callback_data['secret_message_id']),
        }


class ContactDetailCallbackData(CallbackData, ParseContactIdMixin):

    def __init__(self):
        super().__init__('contact-detail', 'contact_id')


class ContactUpdateCallbackData(CallbackData, ParseContactIdMixin):

    def __init__(self):
        super().__init__('contact-update', 'contact_id', 'field')


class ContactDeleteCallbackData(CallbackData, ParseContactIdMixin):

    def __init__(self):
        super().__init__('contact-delete', 'contact_id')
