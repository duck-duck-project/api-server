import random

from django.db.models import Max

from wishes.exceptions import NoWishesError
from wishes.models import Wish

__all__ = ('get_random_wish',)


def get_random_wish(*, max_attempts_count: int = 10) -> Wish:
    max_id = Wish.objects.aggregate(max_id=Max('id'))['max_id']
    if max_id is None:
        raise NoWishesError

    for _ in range(max_attempts_count):
        wish_id = random.randint(1, max_id)
        wish = Wish.objects.filter(id=wish_id).first()

        if wish is not None:
            return wish

    raise NoWishesError
