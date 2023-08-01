from users.exceptions import UserDoesNotExistsError
from users.models import User

__all__ = ('get_user_by_id',)


def get_user_by_id(user_id: int) -> User:
    """Retrieve user instance by ID.

    Args:
        user_id: Telegram ID of user.

    Returns:
        User instance if exists.

    Raises:
        UserDoesNotExistsError: If user does not exist.
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise UserDoesNotExistsError(user_id=user_id)
