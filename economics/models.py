import enum
from dataclasses import dataclass
from uuid import uuid4

from django.db import models

from users.models import User

__all__ = ('OperationPrice', 'Transaction', 'UserBalance')


class OperationPrice(enum.IntEnum):
    RICHEST_USERS = 5000
    CREATE_CONTACT = 100


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sender = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='sender',
        null=True,
        blank=True,
    )
    recipient = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='recipient',
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=(
                        models.Q(sender__isnull=False)
                        | models.Q(recipient__isnull=False)
                ),
                name='either_sender_or_recipient',
                violation_error_message=(
                    'Transaction must have at least either sender or recipient'
                ),
            ),
            models.CheckConstraint(
                check=~models.Q(sender=models.F('recipient')),
                name='sender_not_equal_recipient',
                violation_error_message=(
                    'Sender and recipient must not be equal'
                ),
            ),
        )

    @property
    def is_transfer(self) -> bool:
        return self.sender is not None and self.recipient is not None

    @property
    def is_deposit(self) -> bool:
        return self.recipient is not None and self.sender is None

    @property
    def is_withdrawal(self) -> bool:
        return self.sender is not None and self.recipient is None


# TODO rename fields
@dataclass(frozen=True, slots=True)
class UserBalance:
    user_id: int
    user_fullname: str
    user_username: str | None
    balance: int
