from repositories import APIRepository

__all__ = ('TeamMemberRepository',)


class TeamMemberRepository(APIRepository):

    async def create(self, *, team_id: int, user_id: int) -> None:
        pass

    async def delete_by_id(self, team_member_id: int) -> list[int]:
        pass

    async def get_by_team_id(self, team_id: int) -> list:
        pass
