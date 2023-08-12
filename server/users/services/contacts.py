from django.db import IntegrityError

from users.exceptions import ContactAlreadyExistsError
from users.models import User, Contact

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
    """Create contact.

    Keyword Args:
        of_user: user who adds contact.
        to_user: user who is added to contacts.
        private_name: name of contact that is visible only to user.
        public_name: name of contact that is visible to all users.

    Returns:
        Contact instance.
    """
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
        is_hidden: bool,
) -> bool:
    """Update contact.

    Keyword Args:
        contact_id: id of contact to update.
        private_name: name of contact that is visible only to user.
        public_name: name of contact that is visible to all users.
        is_hidden: whether contact is hidden from user.
    """
    updated_count = Contact.objects.filter(id=contact_id).update(
        private_name=private_name,
        public_name=public_name,
        is_hidden=is_hidden,
    )
    return bool(updated_count)
