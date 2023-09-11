from pydantic import BaseModel

__all__ = ('UserBalance',)


class UserBalance(BaseModel):
    user_id: int
    balance: int
