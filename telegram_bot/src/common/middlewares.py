from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

__all__ = ('DependencyInjectMiddleware',)


class DependencyInjectMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ("update",)

    def __init__(self, **kwargs):
        super().__init__()
        self.__kwargs = kwargs

    async def pre_process(self, obj, data, *args):
        for key, value in self.__kwargs.items():
            data[key] = value
