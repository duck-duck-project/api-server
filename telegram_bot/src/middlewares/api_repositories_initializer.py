import aiohttp
from aiogram import BaseMiddleware
from aiogram.types import Update

from middlewares.common import Handler, ContextData, HandlerReturn
from repositories import APIRepository

__all__ = ('APIRepositoriesInitializerMiddleware',)


class APIRepositoriesInitializerMiddleware(BaseMiddleware):

    def __init__(self, **name_to_api_repository: type[APIRepository]):
        self.__name_to_api_repository = name_to_api_repository

    async def __call__(
            self,
            handler: Handler,
            event: Update,
            data: ContextData,
    ) -> HandlerReturn:
        http_client: aiohttp.ClientSession = data['http_client']
        for name, api_repository_type in self.__name_to_api_repository.items():
            data[name] = api_repository_type(http_client)
        return await handler(event, data)
