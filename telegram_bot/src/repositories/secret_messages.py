from uuid import UUID

import models
from exceptions import SecretMessageDoesNotExistError
from repositories import APIRepository

__all__ = ('SecretMessageRepository',)


class SecretMessageRepository(APIRepository):

    async def create(
            self,
            *,
            secret_message_id: UUID,
            text: str,
    ) -> None:
        request_data = {
            'id': str(secret_message_id),
            'text': text,
        }
        url = '/secret-messages/'
        async with self._http_client.post(url, json=request_data) as response:
            pass

    async def get_by_id(self, secret_message_id: UUID) -> models.SecretMessage:
        url = f'/secret-messages/{str(secret_message_id)}/'
        async with self._http_client.get(url) as response:
            if response.status == 404:
                raise SecretMessageDoesNotExistError
            response_data = await response.json()
        return models.SecretMessage.model_validate(response_data)
