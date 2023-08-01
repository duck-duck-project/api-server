from users.models import User

__all__ = ('upsert_user',)


def upsert_user(
        *,
        user_id: int,
        fullname: str,
        username: str | None,
) -> tuple[User, bool]:
    """Create user or update user if already exists.

    Keyword Args:
        user_id: Telegram ID of user.
        fullname: name of user.
        username: username of user.

    Returns:
        User instance and boolean that indicates
        whether user has been created or not.
    """
    return User.objects.update_or_create(
        id=user_id,
        defaults={
            'fullname': fullname,
            'username': username,
        },
    )
