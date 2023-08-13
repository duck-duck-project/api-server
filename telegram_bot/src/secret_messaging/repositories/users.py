from common.repositories import APIRepository
from secret_messaging import models
from secret_messaging.exceptions import UserDoesNotExistError

__all__ = ('UserRepository',)


class UserRepository(APIRepository):

    async def get_by_id(self, user_id: int) -> models.User:
        url = f'/users/{user_id}/'
        async with self._http_client.get(url) as response:
            if response.status == 404:
                raise UserDoesNotExistError(user_id=user_id)
            response_data = await response.json()
        return models.User.model_validate(response_data)

    async def upsert(
            self,
            *,
            user_id: int,
            fullname: str,
            username: str | None,
            can_be_added_to_contacts: bool | None = None,
    ) -> None:
        request_data = {
            'id': user_id,
            'fullname': fullname,
            'username': username,
        }
        if can_be_added_to_contacts is not None:
            request_data['can_be_added_to_contacts'] = can_be_added_to_contacts

        url = '/users/'
        async with self._http_client.post(url, json=request_data) as response:
            pass
