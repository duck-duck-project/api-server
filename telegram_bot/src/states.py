from aiogram.fsm.state import StatesGroup, State

__all__ = (
    'ContactUpdateStates',
    'SecretMediaCreateStates',
    'AnonymousMessagingStates',
    'TeamCreateStates',
    'TeamDeleteStates',
    'TeamMemberCreateStates',
    'ContactCreateWaitForForwardedMessage',
)


class ContactCreateWaitForForwardedMessage(StatesGroup):
    enabled = State()


class AnonymousMessagingStates(StatesGroup):
    enabled = State()


class ContactUpdateStates(StatesGroup):
    private_name = State()
    public_name = State()


class SecretMediaCreateStates(StatesGroup):
    contact = State()
    media = State()
    description = State()
    confirm = State()


class TeamCreateStates(StatesGroup):
    name = State()


class TeamDeleteStates(StatesGroup):
    confirm = State()


class TeamMemberCreateStates(StatesGroup):
    contact = State()
