from aiogram import BaseMiddleware
from aiogram.types import Update

from middlewares.common import Handler, ContextData, HandlerReturn
from repositories import HTTPClientFactory

__all__ = ('HTTPClientFactoryMiddleware',)


class HTTPClientFactoryMiddleware(BaseMiddleware):

    __slots__ = ('__closing_http_client_factory',)

    def __init__(self, closing_http_client_factory: HTTPClientFactory):
        self.__closing_http_client_factory = closing_http_client_factory

    async def __call__(
            self,
            handler: Handler,
            event: Update,
            data: ContextData,
    ) -> HandlerReturn:
        async with self.__closing_http_client_factory() as http_client:
            data['http_client'] = http_client
            return await handler(event, data)
