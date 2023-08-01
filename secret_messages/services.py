from django.db import IntegrityError

from secret_messages.exceptions import (
    ContactAlreadyExistsError,
    ContactDoesNotExistError
)
from secret_messages.models import Contact
from secret_messages.selectors import get_contact_by_id
from users.models import User

__all__ = (
    'create_contact',
    'update_contact',
)


def create_contact(
        *,
        of_user: User,
        to_user: User,
        private_name: str,
        public_name: str,
) -> Contact:
    try:
        return Contact.objects.create(
            of_user=of_user,
            to_user=to_user,
            private_name=private_name,
            public_name=public_name,
        )
    except IntegrityError as error:
        if 'UNIQUE constraint failed' in str(error):
            raise ContactAlreadyExistsError
        raise


def update_contact(
        *,
        contact_id: int,
        private_name: str,
        public_name: str,
) -> None:
    contacts_to_update = Contact.objects.filter(id=contact_id)
    updated_rows_count = contacts_to_update.update(
        private_name=private_name,
        public_name=public_name,
    )
    if not updated_rows_count:
        raise ContactDoesNotExistError(contact_id=contact_id)
