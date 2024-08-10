import random
from dataclasses import dataclass
from typing import Final, Literal, TypedDict

__all__ = (
    'ResourceStrategy',
    'ENERGY_COST',
    'HEALTH_COST',
    'MINING_RESOURCES_STRATEGIES',
    'MinedResource',
    'get_random_resource_strategy',
    'get_random_mined_resource',
    'get_energy_cost',
    'get_health_cost',
)


class ResourceStrategy(TypedDict):
    name: str
    min_weight_in_grams: int
    max_weight_in_grams: int
    probability: int
    premium_probability: int
    value_per_gram: int | float


MINING_RESOURCES_STRATEGIES: Final[tuple[ResourceStrategy, ...]] = (
    {
        'name': 'Уголь',
        'min_weight_in_grams': 20000,
        'max_weight_in_grams': 80000,
        'probability': 2500,
        'value_per_gram': 0.02,
        'premium_probability': 2125,
    },
    {
        'name': 'Железо',
        'min_weight_in_grams': 10000,
        'max_weight_in_grams': 40000,
        'probability': 1600,
        'value_per_gram': 0.065,
        'premium_probability': 1360,
    },
    {
        'name': 'Медь',
        'min_weight_in_grams': 20000,
        'max_weight_in_grams': 50000,
        'probability': 1300,
        'value_per_gram': 0.03,
        'premium_probability': 1105,
    },
    {
        'name': 'Олово',
        'min_weight_in_grams': 3500,
        'max_weight_in_grams': 5000,
        'probability': 1100,
        'value_per_gram': 0.2,
        'premium_probability': 935,
    },
    {
        'name': 'Никель',
        'min_weight_in_grams': 2000,
        'max_weight_in_grams': 10000,
        'probability': 900,
        'value_per_gram': 0.35,
        'premium_probability': 855,
    },
    {
        'name': 'Серебро',
        'min_weight_in_grams': 800,
        'max_weight_in_grams': 3500,
        'probability': 700,
        'value_per_gram': 0.85,
        'premium_probability': 735,
    },
    {
        'name': 'Литий',
        'min_weight_in_grams': 500,
        'max_weight_in_grams': 2000,
        'probability': 500,
        'value_per_gram': 2.25,
        'premium_probability': 875,
    },
    {
        'name': 'Золото',
        'min_weight_in_grams': 30,
        'max_weight_in_grams': 70,
        'probability': 300,
        'value_per_gram': 85,
        'premium_probability': 445,
    },
    {
        'name': 'Алмаз',
        'min_weight_in_grams': 5,
        'max_weight_in_grams': 20,
        'probability': 100,
        'value_per_gram': 550,
        'premium_probability': 165,
    },
    {
        'name': 'Уран',
        'min_weight_in_grams': 300,
        'max_weight_in_grams': 500,
        'probability': 500,
        'value_per_gram': 6.5,
        'premium_probability': 675,
    },
    {
        'name': 'Платина',
        'min_weight_in_grams': 80,
        'max_weight_in_grams': 100,
        'probability': 300,
        'value_per_gram': 70,
        'premium_probability': 395,
    },
    {
        'name': 'Редкоземельные металлы',
        'min_weight_in_grams': 50,
        'max_weight_in_grams': 200,
        'probability': 200,
        'value_per_gram': 15,
        'premium_probability': 330,
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


ENERGY_COST: Final[int] = 950
HEALTH_COST: Final[int] = 100


def get_energy_cost(is_premium: bool) -> int:
    if is_premium:
        return int(ENERGY_COST * 0.75)
    return ENERGY_COST


def get_health_cost(is_premium: bool) -> int:
    if is_premium:
        return int(HEALTH_COST * 0.8)
    return HEALTH_COST


def get_random_resource_strategy(is_premium: bool) -> ResourceStrategy:
    key: Literal['premium_probability', 'probability'] = (
        'premium_probability' if is_premium else 'probability'
    )
    probabilities = [strategy[key] for strategy in MINING_RESOURCES_STRATEGIES]
    return random.choices(
        MINING_RESOURCES_STRATEGIES,
        weights=probabilities,
    )[0]


def get_random_mined_resource(is_premium: bool) -> MinedResource:
    resource_strategy = get_random_resource_strategy(is_premium)
    mined_resource = MinedResource(
        name=resource_strategy['name'],
        weight_in_grams=random.randint(
            resource_strategy['min_weight_in_grams'],
            resource_strategy['max_weight_in_grams'],
        ),
        value_per_gram=resource_strategy['value_per_gram'],
    )
    return mined_resource
