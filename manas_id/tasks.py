import contextlib

from celery import shared_task
from fast_depends import inject

from economics.services.allowance import create_stipend
from manas_id.selectors import iter_manas_ids


@shared_task
@inject
def give_away_stipends(
) -> None:
    for manas_ids in iter_manas_ids():
        for manas_id in manas_ids:
            with contextlib.suppress(Exception):
                create_stipend(user=manas_id.user)
