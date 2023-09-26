from datetime import date

from django.db import IntegrityError

from users.exceptions import UserAlreadyExistsError
from users.models import User

__all__ = (
    'create_user',
    'update_user',
)


def create_user(
        *,
        user_id: int,
        fullname: str,
        username: str | None,
) -> User:
    """Create user.

    Keyword Args:
        user_id: Telegram ID of user.
        fullname: Full name of user.
        username: Username of user.

    Returns:
        User instance.

    Raises:
        UserAlreadyExistsError: If user already exists.
    """
    try:
        return User.objects.create(
            id=user_id,
            fullname=fullname,
            username=username,
        )
    except IntegrityError:
        raise UserAlreadyExistsError


def update_user(
        *,
        user_id: int,
        fullname: str,
        username: str | None,
        secret_message_theme_id: int | None,
        can_be_added_to_contacts: bool,
        can_receive_notifications: bool,
        born_at: date | None,
        profile_photo_url: str | None,
) -> bool:
    """Update user.

    Keyword Args:
        user_id: Telegram ID of user.
        fullname: Full name of user.
        username: Username of user.
        secret_message_theme_id: ID of secret message theme.
        can_be_added_to_contacts: Boolean that indicates whether user can be
            added to contacts or not.
        can_receive_notifications: Boolean that indicates whether user can
            receive notifications or not.
        born_at: Date of birth of user.
        profile_photo_url: URL of profile photo of user.

    Returns:
        Boolean that indicates whether user has been updated or not.
    """
    updated_count = User.objects.filter(id=user_id).update(
        fullname=fullname,
        username=username,
        secret_message_theme_id=secret_message_theme_id,
        can_be_added_to_contacts=can_be_added_to_contacts,
        can_receive_notifications=can_receive_notifications,
        born_at=born_at,
        profile_photo_url=profile_photo_url,
    )
    return bool(updated_count)
