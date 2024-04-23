from dataclasses import dataclass
from datetime import date

from users.models import Contact

__all__ = ('ContactBirthday', 'get_user_contact_birthdays')


@dataclass(frozen=True, slots=True)
class ContactBirthday:
    user_id: int
    fullname: str
    username: str | None
    born_on: date


def get_user_contact_birthdays(user_id: int) -> list[ContactBirthday]:
    user_contacts = Contact.objects.filter(of_user_id=user_id, is_deleted=False)
    contacts_with_birthdays = (
        user_contacts
        .select_related('to_user')
        .filter(to_user__born_on__isnull=False)
        .values(
            'to_user__id',
            'to_user__fullname',
            'to_user__username',
            'to_user__born_on',
        )
    )
    return [
        ContactBirthday(
            user_id=contact['to_user__id'],
            fullname=contact['to_user__fullname'],
            username=contact['to_user__username'],
            born_on=contact['to_user__born_on'],
        )
        for contact in contacts_with_birthdays
    ]
