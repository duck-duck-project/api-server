from datetime import datetime

from pydantic import BaseModel

from models.users import User

__all__ = ('Contact',)


class Contact(BaseModel):
    id: int
    private_name: str
    public_name: str
    created_at: datetime
    is_hidden: bool
    of_user: User
    to_user: User
