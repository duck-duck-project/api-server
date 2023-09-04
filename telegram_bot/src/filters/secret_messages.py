from aiogram.types import ChosenInlineResult

__all__ = ('secret_message_valid_format_chosen_inline_result_filter',)


def secret_message_valid_format_chosen_inline_result_filter(
        chosen_inline_result: ChosenInlineResult,
) -> bool | dict:
    is_contact = chosen_inline_result.result_id.endswith('?')
    try:
        _, contact_id = chosen_inline_result.result_id.rstrip('?').split('@')
        return {'contact_id': int(contact_id), 'is_contact': is_contact}
    except ValueError:
        return False
