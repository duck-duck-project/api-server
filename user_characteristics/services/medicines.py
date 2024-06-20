from dataclasses import dataclass

from django.db import transaction

from economics.services import create_system_withdrawal
from user_characteristics.models import Medicine
from users.models import User
from users.services.users import increase_user_health

__all__ = ('consume_medicine', 'MedicineConsumptionResult')


@dataclass(frozen=True, slots=True)
class MedicineConsumptionResult:
    user_id: int
    medicine_name: str
    price: int
    health_benefit_value: int
    user_health: int


@transaction.atomic
def consume_medicine(
        *,
        user: User,
        medicine: Medicine,
) -> MedicineConsumptionResult:
    withdrawal = create_system_withdrawal(
        user=user,
        amount=medicine.price,
        description=f'Употребление лекарства {medicine.name}',
    )
    user = increase_user_health(
        user=user,
        increase=medicine.health_benefit_value
    )
    return MedicineConsumptionResult(
        user_id=user.id,
        medicine_name=medicine.name,
        price=withdrawal.amount,
        health_benefit_value=medicine.health_benefit_value,
        user_health=user.health,
    )
