from collections.abc import Generator

from django.db.models import QuerySet

from users.exceptions import UserDoesNotExistsError
from users.models import User

__all__ = (
    'get_user_by_id',
    'iter_users_with_birthdays',
)


def get_user_by_id(user_id: int) -> User:
    """Retrieve user instance by ID. Also select related secret message theme.

    Args:
        user_id: Telegram ID of user.

    Returns:
        User instance if exists.

    Raises:
        UserDoesNotExistsError: If user does not exist.
    """
    try:
        return (
            User
            .objects
            .select_related('theme')
            .get(id=user_id)
        )
    except User.DoesNotExist:
        raise UserDoesNotExistsError(user_id=user_id)


def iter_users_with_birthdays(
        *,
        limit: int = 50,
) -> Generator[QuerySet[User], None, None]:
    offset: int = 0

    while True:
        users_with_birthdays = User.objects.exclude(born_on__isnull=True)

        ordered_by_id = users_with_birthdays.order_by('id')

        limited_users = ordered_by_id[offset:offset + limit + 1]

        yield limited_users[:limit]

        if len(limited_users) < limit:
            break

        offset += limit
