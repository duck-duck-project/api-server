from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, InlineQuery, Message

from exceptions import UserDoesNotExistError
from repositories import HTTPClientFactory, UserRepository

__all__ = ('DependencyInjectMiddleware', 'UserMiddleware')


class DependencyInjectMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ("update",)

    def __init__(self, **kwargs):
        super().__init__()
        self.__kwargs = kwargs

    async def pre_process(self, obj, data, *args):
        for key, value in self.__kwargs.items():
            data[key] = value


class UserMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ('update', 'error')

    async def pre_process(
            self,
            obj: Message | CallbackQuery | InlineQuery,
            data: dict,
            *args,
    ):
        closing_http_client_factory: HTTPClientFactory = (
            data['closing_http_client_factory']
        )
        async with closing_http_client_factory() as http_client:
            user_repository = UserRepository(http_client)
            try:
                user = await user_repository.get_by_id(obj.from_user.id)
            except UserDoesNotExistError:
                user = await user_repository.create(
                    user_id=obj.from_user.id,
                    fullname=obj.from_user.full_name,
                    username=obj.from_user.username,
                )
            data['user'] = user
