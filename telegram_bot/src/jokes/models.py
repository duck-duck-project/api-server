from dataclasses import dataclass
from datetime import datetime

__all__ = ('Joke', 'JokeStatistics')


@dataclass(frozen=True, slots=True)
class Joke:
    id: int
    text: str
    user_id: int
    joked_at: datetime
    registered_by_user_id: int


@dataclass(frozen=True, slots=True)
class JokeStatistics:
    user_id: int
    count: int
