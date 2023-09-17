from dataclasses import dataclass

__all__ = ('InsufficientFundsForSystemWithdrawalError',)


@dataclass(frozen=True, slots=True)
class InsufficientFundsForSystemWithdrawalError(Exception):
    user_id: int
    amount: int
    balance: int
    description: str

    def __str__(self) -> str:
        return (
            f'User {self.user_id} has insufficient funds'
            f' for system withdrawal of {self.amount}.'
            f' Balance: {self.balance}.'
            f' Transaction: {self.description}.'
        )
