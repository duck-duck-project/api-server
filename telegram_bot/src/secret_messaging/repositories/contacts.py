from pydantic import TypeAdapter

from common.repositories import APIRepository
from secret_messaging import models

__all__ = ('ContactRepository',)


class ContactRepository(APIRepository):

    async def upsert(
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
                raise
            response_data = await response.json()
        return models.Contact.model_validate(response_data)

    async def get_by_user_id(
            self,
            user_id: int,
    ) -> list[models.Contact]:
        url = f'/contacts/users/{user_id}/'
        async with self._http_client.get(url) as response:
            response_data = await response.json()
        type_adapter = TypeAdapter(list[models.Contact])
        return type_adapter.validate_python(response_data)

    async def get_by_id(self, contact_id: int) -> models.Contact:
        url = f'/contacts/{contact_id}/'
        async with self._http_client.get(url) as response:
            response_data = await response.json()
        return models.Contact.model_validate(response_data)

    async def update(
            self,
            *,
            contact_id: int,
            private_name: str,
            public_name: str,
            is_hidden: bool | None = None,
    ) -> None:
        url = f'/contacts/{contact_id}/'
        request_data = {
            'private_name': private_name,
            'public_name': public_name,
        }
        if is_hidden is not None:
            request_data['is_hidden'] = is_hidden
        async with self._http_client.put(url, json=request_data):
            pass

    async def delete_by_id(self, contact_id: int) -> None:
        url = f'/contacts/{contact_id}/'
        async with self._http_client.delete(url):
            pass
