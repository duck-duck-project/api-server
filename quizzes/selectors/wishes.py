import random

from rest_framework.exceptions import NotFound

from quizzes.exceptions import WishNotFoundError
from quizzes.models import Wish

__all__ = ('get_random_wish_text',)


def get_random_wish_text() -> str:
    """
    Get random wish text.

    Returns:
        Wish object.

    Raises:
        WishNotFoundError - if there are no wish.
    """
    wish_ids = Wish.objects.values_list('id', flat=True)
    if not wish_ids:
        raise WishNotFoundError

    try:
        return Wish.objects.get(id=random.choice(wish_ids)).text
    except Wish.DoesNotExist:
        raise WishNotFoundError
