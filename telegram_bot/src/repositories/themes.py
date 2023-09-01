from exceptions import ServerAPIError, ThemeDoesNotExistError
from models import ThemesPage, SecretMessageTheme
from repositories.base import APIRepository

__all__ = ('ThemeRepository',)


class ThemeRepository(APIRepository):

    async def get_all(
            self,
            *,
            limit: int | None = None,
            offset: int | None = None,
    ) -> ThemesPage:
        request_query_params = {}
        if limit is not None and offset is not None:
            request_query_params['limit'] = limit
            request_query_params['offset'] = offset

        async with self._http_client.get(
                url='/themes/',
                params=request_query_params,
        ) as response:
            if response.status != 200:
                raise ServerAPIError
            response_data = await response.json()
        return ThemesPage.model_validate(response_data)

    async def get_by_id(self, theme_id: int) -> SecretMessageTheme:
        url = f'/themes/{theme_id}/'
        async with self._http_client.get(url) as response:
            if response.status == 404:
                raise ThemeDoesNotExistError
            if response.status != 200:
                raise ServerAPIError
            response_data = await response.json()
        return SecretMessageTheme.model_validate(response_data)
