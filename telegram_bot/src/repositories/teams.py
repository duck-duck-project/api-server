from models import TeamIdAndName
from repositories import APIRepository

__all__ = ('TeamRepository',)


class TeamRepository(APIRepository):

    async def create(self, *, user_id: int, name: str):
        pass

    async def get_by_user_id(self, user_id: int) -> list[TeamIdAndName]:
        pass

    async def get_by_id(self, team_id: int):
        pass

    async def delete_by_id(self, team_id: int) -> None:
        pass
