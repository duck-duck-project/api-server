from datetime import date

from pydantic import BaseModel, HttpUrl

from models.themes import SecretMessageTheme

__all__ = ('User',)


class User(BaseModel):
    id: int
    fullname: str
    username: str | None
    is_premium: bool
    can_be_added_to_contacts: bool
    secret_message_theme: SecretMessageTheme | None
    profile_photo_url: HttpUrl | None
    is_banned: bool
    can_receive_notifications: bool
    born_at: date | None
