from pydantic import TypeAdapter

from exceptions import ServerAPIError
from models import TeamIdAndName, Team
from repositories import APIRepository

__all__ = ('TeamRepository',)


class TeamRepository(APIRepository):

    async def create(self, *, user_id: int, name: str) -> Team:
        url = f'/users/{user_id}/teams/'
        request_data = {'name': name}
        response = await self._http_client.post(url, json=request_data)
        if response.status != 201:
            raise ServerAPIError
        response_data = await response.json()
        return Team.model_validate(response_data)

    async def get_by_user_id(self, user_id: int) -> list[TeamIdAndName]:
        url = f'/users/{user_id}/teams/'
        response = await self._http_client.get(url)
        if response.status != 200:
            raise ServerAPIError
        response_data = await response.json()
        type_adapter = TypeAdapter(list[TeamIdAndName])
        return type_adapter.validate_python(response_data)

    async def get_by_id(self, team_id: int) -> Team:
        url = f'/teams/{team_id}/'
        response = await self._http_client.get(url)
        if response.status != 200:
            raise ServerAPIError
        response_data = await response.json()
        return Team.model_validate(response_data)

    async def delete_by_id(self, team_id: int) -> None:
        url = f'/teams/{team_id}/'
        response = await self._http_client.delete(url)
        if response.status != 204:
            raise ServerAPIError
