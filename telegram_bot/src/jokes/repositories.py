from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from common.repositories import APIRepository
from jokes import models
from jokes.database import Joke
from jokes.exceptions import JokeAlreadyExists

__all__ = ('JokeRepository',)


def map_to_dto(joke: Joke) -> models.Joke:
    return models.Joke(
        id=joke.id,
        user_id=joke.user_id,
        text=joke.text,
        joked_at=joke.joked_at,
        registered_by_user_id=joke.registered_by_user_id,
    )


class JokeRepository(APIRepository):

    async def create(
            self,
            *,
            user_id: int,
            text: str,
            joked_at: datetime,
            registered_by_user_id: int,
    ) -> models.Joke:
        joke = Joke(
            user_id=user_id,
            text=text,
            joked_at=joked_at,
            registered_by_user_id=registered_by_user_id,
        )
        try:
            async with self._session_factory() as session:
                async with session.begin():
                    session.add(joke)
                    await session.flush()
                    await session.refresh(joke)
                    return map_to_dto(joke)
        except IntegrityError:
            raise JokeAlreadyExists

    async def count_by_users(self):
        statement = (
            select(func.count(Joke.id), Joke.user_id)
            .group_by(Joke.user_id)
        )
        with self._session_factory() as session:
            result = await session.execute(statement)
            rows = result.all()
        return [
            models.JokeStatistics(
                count=count,
                user_id=user_id,
            ) for count, user_id in rows
        ]
