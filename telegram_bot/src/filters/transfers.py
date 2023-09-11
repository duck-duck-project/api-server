from aiogram.types import Message

__all__ = (
    'transfer_operation_amount_filter',
)


def transfer_operation_amount_filter(message: Message) -> bool | dict:
    try:
        _, amount = message.text.split(' ')
        return {'amount': int(amount)}
    except ValueError:
        return False
