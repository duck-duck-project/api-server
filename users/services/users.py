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
) -> bool:
    """Update user.

    Keyword Args:
        user_id: Telegram ID of user.
        fullname: Full name of user.
        username: Username of user.

    Returns:
        Boolean that indicates whether user has been updated or not.
    """
    updated_count = User.objects.filter(id=user_id).update(
        fullname=fullname,
        username=username,
    )
    return bool(updated_count)
