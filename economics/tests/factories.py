from factory.django import DjangoModelFactory

from economics.models import Transaction

__all__ = (
    'TransferFactory',
    'SystemDepositFactory',
    'SystemWithdrawalFactory',
)


class TransferFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    source = Transaction.Source.TRANSFER


class SystemDepositFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    sender = None
    source = Transaction.Source.SYSTEM


class SystemWithdrawalFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    recipient = None
    source = Transaction.Source.SYSTEM
