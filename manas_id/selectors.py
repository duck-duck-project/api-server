from collections.abc import Generator

from django.db.models import QuerySet

from manas_id.exceptions import ManasIdDoesNotExistError
from manas_id.models import ManasId

__all__ = ('get_manas_id_by_user_id', 'iter_manas_ids')


def get_manas_id_by_user_id(user_id: int) -> ManasId:
    try:
        return (
            ManasId.objects
            .select_related('department')
            .get(user_id=user_id)
        )
    except ManasId.DoesNotExist:
        raise ManasIdDoesNotExistError


def iter_manas_ids(
        limit: int = 100,
) -> Generator[QuerySet[ManasId], None, None]:
    offset = 0
    while True:
        manas_ids = ManasId.objects.select_related('user')[offset:limit + 1]
        yield manas_ids[:limit]
        offset += limit
        if len(manas_ids) < limit:
            break
