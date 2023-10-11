import enum
from dataclasses import dataclass
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models

from users.models import User

__all__ = ('OperationPrice', 'Transaction', 'UserBalance')


class OperationPrice(enum.IntEnum):
    RICHEST_USERS = 5000


class Transaction(models.Model):

    class Source(models.IntegerChoices):
        TRANSFER = 1
        SYSTEM = 2

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
    source = models.PositiveSmallIntegerField(choices=Source.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def full_clean(
            self,
            exclude=None,
            validate_unique=True,
            validate_constraints=True,
    ):
        super().full_clean(
            exclude=exclude,
            validate_unique=validate_unique,
            validate_constraints=validate_constraints,
        )

        if self.source == Transaction.Source.TRANSFER:
            if self.sender is None or self.recipient is None:
                raise ValidationError(
                    'Transfer transaction must have both sender and recipient',
                )
        if self.source == Transaction.Source.SYSTEM:
            if self.sender is not None and self.recipient is not None:
                raise ValidationError(
                    'System transaction can not have both sender and recipient',
                )
            if self.sender is None and self.recipient is None:
                raise ValidationError(
                    'System transaction must have either sender or recipient',
                )


# TODO rename fields
@dataclass(frozen=True, slots=True)
class UserBalance:
    user_id: int
    user_fullname: str
    user_username: str | None
    balance: int
