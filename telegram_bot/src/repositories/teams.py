from models import Team
from repositories import APIRepository

__all__ = ('TeamRepository',)


class TeamRepository(APIRepository):

    async def create(self, *, user_id: int, name: str) -> Team:
        pass

    async def get_by_user_id(self, user_id: int) -> list[Team]:
        pass

    async def get_by_id(self, team_id: int) -> Team:
        pass
