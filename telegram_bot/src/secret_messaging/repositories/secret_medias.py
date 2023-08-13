from uuid import UUID

from pydantic import TypeAdapter

from common.repositories import APIRepository
from secret_messaging import models
from secret_messaging.exceptions import (
    SecretMediaAlreadyExistsError,
    SecretMediaDoesNotExistError,
)

__all__ = ('SecretMediaRepository',)


class SecretMediaRepository(APIRepository):

    async def create(
            self,
            media_type: int,
            file_id: str,
            description: str | None,
            contact_id: int,
    ) -> models.SecretMedia:
        url = '/secret-medias/'
        request_data = {
            'media_type': media_type,
            'file_id': file_id,
            'name': description,
            'contact_id': contact_id,
        }
        async with self._http_client.post(url, json=request_data) as response:
            if response.status == 409:
                raise SecretMediaAlreadyExistsError
            response_data = await response.json()
        return models.SecretMedia.model_validate(response_data)

    async def get_by_id(self, secret_media_id: UUID) -> models.SecretMedia:
        url = f'/secret-medias/{secret_media_id}/'
        async with self._http_client.get(url) as response:
            if response.status == 404:
                raise SecretMediaDoesNotExistError
            response_data = await response.json()
        return models.SecretMedia.model_validate(response_data)

    async def get_by_user_id(
            self,
            user_id: int,
            media_type: int | None = None,
    ) -> list[models.SecretMedia]:
        url = f'/secret-medias/users/{user_id}/'
        request_query_params = {}
        if media_type is not None:
            request_query_params['media_type'] = media_type
        async with self._http_client.get(url) as response:
            response_data = await response.json()
        type_adapter = TypeAdapter(list[models.SecretMedia])
        return type_adapter.validate_python(response_data)
