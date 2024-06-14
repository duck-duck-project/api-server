import random
from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias

from django.db import transaction
from django.utils import timezone

from economics.services import create_system_deposit
from mining.exceptions import MiningActionThrottledError
from mining.models import MiningAction

__all__ = (
    'get_last_mining_action',
    'create_mining_action',
    'get_random_resource',
    'MiningResource',
    'ResourceAndProbability',
    'MINING_RESOURCES_AND_PROBABILITIES',
)

from users.models import User


@dataclass(frozen=True, slots=True)
class MiningResource:
    name: str
    min_wealth: int
    max_wealth: int

    def compute_wealth(self) -> int:
        return random.randint(self.min_wealth, self.max_wealth)


ResourceAndProbability: TypeAlias = tuple[MiningResource, int]

MINING_RESOURCES_AND_PROBABILITIES: tuple[ResourceAndProbability, ...] = (
    (MiningResource(name='Уголь', min_wealth=50, max_wealth=500), 20),
    (MiningResource(name='Железо', min_wealth=100, max_wealth=1000), 15),
    (MiningResource(name='Золото', min_wealth=500, max_wealth=5000), 10),
    (MiningResource(name='Алмаз', min_wealth=1000, max_wealth=10000), 5),
    (MiningResource(name='Платина', min_wealth=1500, max_wealth=15000), 3),
    (MiningResource(name='Медь', min_wealth=200, max_wealth=2000), 12),
    (MiningResource(name='Олово', min_wealth=100, max_wealth=1000), 10),
    (MiningResource(name='Серебро', min_wealth=300, max_wealth=3000), 8),
    (MiningResource(name='Никель', min_wealth=200, max_wealth=2000), 7),
    (MiningResource(name='Литий', min_wealth=500, max_wealth=5000), 5),
    (MiningResource(name='Уран', min_wealth=1000, max_wealth=10000), 3),
    (MiningResource(name='Редкоземельные металлы', min_wealth=500,
                    max_wealth=5000), 2)
)


def get_random_resource() -> MiningResource:
    resources = [resource for resource, _ in MINING_RESOURCES_AND_PROBABILITIES]
    probabilities = [
        probability for _, probability in
        MINING_RESOURCES_AND_PROBABILITIES
    ]
    return random.choices(resources, probabilities)[0]


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


def validate_mining_time(next_mining_at: datetime) -> None:
    time_before_next_mining = next_mining_at - timezone.now()
    next_mining_in_seconds = int(time_before_next_mining.total_seconds())
    if next_mining_in_seconds > 0:
        raise MiningActionThrottledError(next_mining_in_seconds)


@transaction.atomic
def create_mining_action(*, user: User) -> MiningAction:
    mined_resource = get_random_resource()
    wealth = mined_resource.compute_wealth()

    last_mining_action = get_last_mining_action(user_id=user.id)

    if last_mining_action is not None:
        validate_mining_time(last_mining_action.next_mining_at)

    mining_action = MiningAction.objects.create(
        user_id=user.id,
        resource_name=mined_resource.name,
        wealth=wealth,
    )
    create_system_deposit(
        user=user,
        description=f'⛏️ Работа на шахте ({mining_action.resource_name})',
        amount=mining_action.wealth,
    )
    return mining_action
