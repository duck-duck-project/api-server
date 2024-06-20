from typing import TypedDict

from user_characteristics.exceptions import MedicineDoesNotExistError
from user_characteristics.models import Medicine

__all__ = ('MedicineTypedDict', 'get_medicines', 'get_medicine_by_name')


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


def get_medicine_by_name(medicine_name: str) -> Medicine:
    try:
        return Medicine.objects.get(name__iexact=medicine_name)
    except Medicine.DoesNotExist:
        raise MedicineDoesNotExistError(medicine_name)
