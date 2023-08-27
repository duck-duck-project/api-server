from pydantic import TypeAdapter

from exceptions import ServerAPIError
from models import TeamMember
from repositories import APIRepository

__all__ = ('TeamMemberRepository',)


class TeamMemberRepository(APIRepository):

    async def create(self, *, team_id: int, user_id: int) -> TeamMember:
        url = f'/teams/{team_id}/members/'
        request_data = {'user_id': user_id}
        response = await self._http_client.post(url, json=request_data)
        if response.status != 201:
            raise ServerAPIError
        response_data = await response.json()
        return TeamMember.model_validate(response_data)

    async def delete_by_id(self, team_member_id: int) -> None:
        url = f'/team-members/{team_member_id}/'
        response = await self._http_client.delete(url)
        if response.status != 204:
            raise ServerAPIError

    async def get_by_team_id(self, team_id: int) -> list[TeamMember]:
        url = f'/teams/{team_id}/members/'
        response = await self._http_client.get(url)
        if response.status != 200:
            raise ServerAPIError
        response_data = await response.json()
        type_adapter = TypeAdapter(list[TeamMember])
        return type_adapter.validate_python(response_data)

    async def get_by_id(self, team_member_id: int) -> TeamMember:
        url = f'/team-members/{team_member_id}/'
        response = await self._http_client.get(url)
        if response.status != 200:
            raise ServerAPIError
        response_data = await response.json()
        return TeamMember.model_validate(response_data)
