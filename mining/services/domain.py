import random
from dataclasses import dataclass
from typing import Final, TypedDict

__all__ = (
    'ResourceStrategy',
    'ENERGY_COST',
    'HEALTH_COST',
    'MINING_RESOURCES_STRATEGIES',
    'MinedResource',
    'get_random_resource_strategy',
    'get_random_mined_resource',
)


class ResourceStrategy(TypedDict):
    name: str
    min_weight_in_grams: int
    max_weight_in_grams: int
    probability: int
    value_per_gram: int | float


MINING_RESOURCES_STRATEGIES: Final[tuple[ResourceStrategy, ...]] = (
    {
        'name': 'Уголь',
        'min_weight_in_grams': 20000,
        'max_weight_in_grams': 80000,
        'probability': 2500,
        'value_per_gram': 0.02,
    },
    {
        'name': 'Железо',
        'min_weight_in_grams': 10000,
        'max_weight_in_grams': 40000,
        'probability': 1600,
        'value_per_gram': 0.065,
    },
    {
        'name': 'Медь',
        'min_weight_in_grams': 20000,
        'max_weight_in_grams': 50000,
        'probability': 1300,
        'value_per_gram': 0.03,
    },
    {
        'name': 'Олово',
        'min_weight_in_grams': 3500,
        'max_weight_in_grams': 5000,
        'probability': 1100,
        'value_per_gram': 0.2,
    },
    {
        'name': 'Никель',
        'min_weight_in_grams': 2000,
        'max_weight_in_grams': 10000,
        'probability': 900,
        'value_per_gram': 0.35,
    },
    {
        'name': 'Серебро',
        'min_weight_in_grams': 800,
        'max_weight_in_grams': 3500,
        'probability': 700,
        'value_per_gram': 0.85,
    },
    {
        'name': 'Литий',
        'min_weight_in_grams': 500,
        'max_weight_in_grams': 2000,
        'probability': 500,
        'value_per_gram': 2.25,
    },
    {
        'name': 'Золото',
        'min_weight_in_grams': 30,
        'max_weight_in_grams': 70,
        'probability': 300,
        'value_per_gram': 85,
    },
    {
        'name': 'Алмаз',
        'min_weight_in_grams': 5,
        'max_weight_in_grams': 20,
        'probability': 100,
        'value_per_gram': 550,
    },
    {
        'name': 'Уран',
        'min_weight_in_grams': 300,
        'max_weight_in_grams': 500,
        'probability': 500,
        'value_per_gram': 6.5,
    },
    {
        'name': 'Платина',
        'min_weight_in_grams': 80,
        'max_weight_in_grams': 100,
        'probability': 300,
        'value_per_gram': 70,
    },
    {
        'name': 'Редкоземельные металлы',
        'min_weight_in_grams': 50,
        'max_weight_in_grams': 200,
        'probability': 200,
        'value_per_gram': 15,
    },
)


@dataclass(frozen=True, slots=True)
class MinedResource:
    name: str
    weight_in_grams: int
    value_per_gram: int | float

    @property
    def value(self) -> int:
        computed_value = int(self.weight_in_grams * self.value_per_gram)
        return computed_value if computed_value != 0 else 1


ENERGY_COST: Final[int] = 1350
HEALTH_COST: Final[int] = 150


def get_random_resource_strategy() -> ResourceStrategy:
    probabilities = [
        strategy['probability']
        for strategy in MINING_RESOURCES_STRATEGIES
    ]
    return random.choices(
        MINING_RESOURCES_STRATEGIES,
        weights=probabilities,
    )[0]


def get_random_mined_resource() -> MinedResource:
    resource_strategy = get_random_resource_strategy()
    mined_resource = MinedResource(
        name=resource_strategy['name'],
        weight_in_grams=random.randint(
            resource_strategy['min_weight_in_grams'],
            resource_strategy['max_weight_in_grams'],
        ),
        value_per_gram=resource_strategy['value_per_gram'],
    )
    return mined_resource
