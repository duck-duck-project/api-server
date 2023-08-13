from pydantic import TypeAdapter

import models
from exceptions import (
    UserDoesNotExistError,
    ContactAlreadyExistsError,
    ServerAPIError,
    ContactDoesNotExistError,
)
from repositories.base import APIRepository

__all__ = ('ContactRepository',)


class ContactRepository(APIRepository):

    async def create(
            self,
            *,
            of_user_id: int,
            to_user_id: int,
            private_name: str,
            public_name: str
    ) -> models.Contact:
        request_data = {
            'of_user_id': of_user_id,
            'to_user_id': to_user_id,
            'private_name': private_name,
            'public_name': public_name,
        }
        url = '/contacts/'
        async with self._http_client.post(url, json=request_data) as response:
            if response.status == 404:
                raise UserDoesNotExistError(user_id=of_user_id)
            if response.status == 409:
                raise ContactAlreadyExistsError
            if response.status != 201:
                raise ServerAPIError
            response_data = await response.json()
        return models.Contact.model_validate(response_data)

    async def get_by_user_id(
            self,
            user_id: int,
    ) -> list[models.Contact]:
        url = f'/users/{user_id}/contacts/'
        async with self._http_client.get(url) as response:
            if response.status != 200:
                raise ServerAPIError
            response_data = await response.json()
        type_adapter = TypeAdapter(list[models.Contact])
        return type_adapter.validate_python(response_data)

    async def get_by_id(self, contact_id: int) -> models.Contact:
        url = f'/contacts/{contact_id}/'
        async with self._http_client.get(url) as response:
            if response.status == 404:
                raise ContactDoesNotExistError(contact_id=contact_id)
            response_data = await response.json()
        return models.Contact.model_validate(response_data)

    async def update(
            self,
            *,
            contact_id: int,
            private_name: str,
            public_name: str,
            is_hidden: bool,
    ) -> None:
        url = f'/contacts/{contact_id}/'
        request_data = {
            'private_name': private_name,
            'public_name': public_name,
            'is_hidden': is_hidden,
        }
        async with self._http_client.put(url, json=request_data) as response:
            if response.status == 404:
                raise ContactDoesNotExistError(contact_id=contact_id)
            if response.status != 204:
                raise ServerAPIError

    async def delete_by_id(self, contact_id: int) -> None:
        url = f'/contacts/{contact_id}/'
        async with self._http_client.delete(url) as response:
            if response.status == 404:
                raise ContactDoesNotExistError(contact_id=contact_id)
            if response.status != 204:
                raise ServerAPIError
