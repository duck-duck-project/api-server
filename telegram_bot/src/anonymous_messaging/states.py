from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ('AnonymousMessagingStates',)


class AnonymousMessagingStates(StatesGroup):
    enabled = State()
