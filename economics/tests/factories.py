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


class SystemDepositFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    sender = None


class SystemWithdrawalFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    recipient = None
