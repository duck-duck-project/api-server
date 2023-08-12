from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = (
    'ContactUpdateStates',
    'SecretMediaCreateStates',
)


class ContactUpdateStates(StatesGroup):
    private_name = State()
    public_name = State()


class SecretMediaCreateStates(StatesGroup):
    contact = State()
    media = State()
    description = State()
    confirm = State()
