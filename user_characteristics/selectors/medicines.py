from typing import TypedDict

from user_characteristics.models import Medicine

__all__ = ('MedicineTypedDict', 'get_medicines')


class MedicineTypedDict(TypedDict):
    name: str
    emoji: str | None
    health_benefit_value: int
    price: int


def get_medicines() -> tuple[MedicineTypedDict, ...]:
    return tuple(
        Medicine.objects
        .values(
            'name',
            'emoji',
            'health_benefit_value',
            'price',
        )
    )
