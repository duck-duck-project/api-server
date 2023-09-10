from collections.abc import Callable, MutableMapping, Awaitable
from typing import TypeAlias, Any

from aiogram.types import Update

__all__ = ('ContextData', 'Handler', 'HandlerReturn')

ContextData: TypeAlias = MutableMapping[str, Any]
Handler: TypeAlias = Callable[[Update, ContextData], Awaitable[Any]]
HandlerReturn: TypeAlias = Any
