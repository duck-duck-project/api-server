import random

from rest_framework.exceptions import NotFound

from quizzes.models import Wish

__all__ = ('get_random_wish',)


def get_random_wish() -> Wish:
    wish_ids = Wish.objects.values_list('id', flat=True)
    if not wish_ids:
        raise NotFound('No wishes found')

    try:
        return Wish.objects.get(id=random.choice(wish_ids))
    except Wish.DoesNotExist:
        raise NotFound('No wishes found')
