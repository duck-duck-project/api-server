from collections.abc import Callable
from typing import TypeAlias

import aiohttp
from redis.asyncio import Redis

__all__ = (
    'HTTPClientFactory',
    'APIRepository',
    'RedisRepository',
)

HTTPClientFactory: TypeAlias = Callable[..., aiohttp.ClientSession]


class APIRepository:

    def __init__(self, http_client: aiohttp.ClientSession):
        self._http_client = http_client


class RedisRepository:

    def __init__(self, redis: Redis):
        self._redis = redis
