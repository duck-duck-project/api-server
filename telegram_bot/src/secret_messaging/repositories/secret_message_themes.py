from pydantic import TypeAdapter

from common.repositories import APIRepository
from secret_messaging.models import SecretMessageTheme

__all__ = ('SecretMessageThemeRepository',)


class SecretMessageThemeRepository(APIRepository):

    async def get_all(self) -> list[SecretMessageTheme]:
        url = '/secret-message-themes/'
        async with self._http_client.get(url) as response:
            response_data: list[dict] = await response.json()
        type_adapter = TypeAdapter(list[SecretMessageTheme])
        return type_adapter.validate_python(response_data)

    async def get_by_id(
            self,
            secret_message_theme_id: int,
    ) -> SecretMessageTheme:
        url = f'/secret-message-themes/{secret_message_theme_id}/'
        async with self._http_client.get(url) as response:
            response_data: dict = await response.json()
        return SecretMessageTheme.model_validate(response_data)
