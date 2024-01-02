from manas_id.exceptions import ManasIdDoesNotExistError
from manas_id.models import ManasId

__all__ = ('get_manas_id_by_user_id',)


def get_manas_id_by_user_id(user_id: int) -> ManasId:
    try:
        return (
            ManasId.objects
            .select_related('department')
            .get(user_id=user_id)
        )
    except ManasId.DoesNotExist:
        raise ManasIdDoesNotExistError
