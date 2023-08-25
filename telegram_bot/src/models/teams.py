import enum
from datetime import datetime

from pydantic import BaseModel

from models.users import User

__all__ = (
    'TeamIdAndName',
    'TeamMember',
    'TeamMemberStatus',
    'Team',
)


class TeamMemberStatus(enum.IntEnum):
    MEMBER = 1
    OWNER = 2


class TeamMember(BaseModel):
    id: int
    name: str
    user_id: int
    status: TeamMemberStatus


class Team(BaseModel):
    id: int
    name: str
    members_count: int
    created_at: datetime


class TeamIdAndName(BaseModel):
    id: int
    name: str
