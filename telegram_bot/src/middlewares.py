from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, InlineQuery, Message, ChatType

from exceptions import UserDoesNotExistError
from models import User
from repositories import HTTPClientFactory, UserRepository
from views import UserBannedInlineQueryView

__all__ = (
    'DependencyInjectMiddleware',
    'UserMiddleware',
    'BannedUsersFilterMiddleware',
)


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
        if isinstance(obj, Message):
            if obj.get_command() is None and obj.chat.type != ChatType.PRIVATE:
                return

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


class BannedUsersFilterMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ('update', 'error')

    async def pre_process(
            self,
            obj: Message | CallbackQuery | InlineQuery,
            data: dict,
            *args,
    ) -> None:
        if isinstance(obj, Message):
            if obj.get_command() is None:
                return

        user: User = data['user']
        text = 'Вы были заблокированы в боте и не можете его использовать'
        if user.is_banned:
            match obj:
                case Message():
                    await obj.answer(text)
                case CallbackQuery():
                    await obj.answer(text, show_alert=True)
                case InlineQuery():
                    items = [
                        UserBannedInlineQueryView()
                        .get_inline_query_result_article()
                    ]
                    await obj.answer(items, is_personal=True)
            raise CancelHandler
