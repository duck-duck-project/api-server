from mining.models import MiningAction

__all__ = ('get_last_mining_action',)


def get_last_mining_action(
        *,
        user_id: int,
) -> MiningAction | None:
    return (
        MiningAction.objects
        .filter(user_id=user_id)
        .order_by('-created_at')
        .first()
    )
