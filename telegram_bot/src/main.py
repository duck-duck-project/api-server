import asyncio
import pathlib
from functools import partial

import aiohttp
import cloudinary
import humanize
import sentry_sdk
import structlog
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import ClientTimeout
from redis.asyncio import Redis
from structlog.stdlib import BoundLogger

import handlers
from config import load_config_from_file_path
from logger import setup_logging
from middlewares import (
    HTTPClientFactoryMiddleware,
    APIRepositoriesInitializerMiddleware,
    user_retrieve_middleware,
    banned_users_middleware,
)
from repositories import (
    UserRepository, ContactRepository,
    SecretMediaRepository, SecretMessageRepository, TeamMemberRepository,
    TeamRepository, TransferRepository
)
from repositories.themes import ThemeRepository

logger: BoundLogger = structlog.get_logger('app')


def include_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        handlers.countdown.router,
        handlers.food_menu.router,
        handlers.premium.router,
        handlers.server.router,
        handlers.users.router,
        handlers.teams.router,
        handlers.team_members.router,
        handlers.themes.router,
        handlers.transfers.router,
        handlers.secret_messages.router,
        handlers.secret_medias.router,
        handlers.contacts.router,
        handlers.anonymous_messages.router,
        handlers.common.router,
    )


async def main() -> None:
    humanize.i18n.activate('ru_RU')

    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config_from_file_path(config_file_path)

    setup_logging(config.logging.level)

    cloudinary.config(
        cloud_name=config.cloudinary.cloud_name,
        api_key=config.cloudinary.api_key,
        api_secret=config.cloudinary.api_secret,
    )

    redis = Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
    )
    storage = RedisStorage(redis)

    bot = Bot(token=config.telegram_bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(storage=storage)

    dispatcher['closing_http_client_factory'] = partial(
        aiohttp.ClientSession,
        base_url=config.server_api_base_url,
        timeout=ClientTimeout(60),
    )
    dispatcher['chat_id_for_retranslation'] = config.main_chat_id
    dispatcher['timezone'] = config.timezone

    include_routers(dispatcher)

    dispatcher.update.outer_middleware(HTTPClientFactoryMiddleware(
        dispatcher['closing_http_client_factory'],
    ))
    dispatcher.update.outer_middleware(
        APIRepositoriesInitializerMiddleware(
            contact_repository=ContactRepository,
            secret_media_repository=SecretMediaRepository,
            secret_message_repository=SecretMessageRepository,
            team_member_repository=TeamMemberRepository,
            team_repository=TeamRepository,
            theme_repository=ThemeRepository,
            transfer_repository=TransferRepository,
            user_repository=UserRepository,
        )
    )
    dispatcher.update.outer_middleware(user_retrieve_middleware)
    dispatcher.update.middleware(banned_users_middleware)

    if config.sentry.is_enabled:
        sentry_sdk.init(
            dsn=config.sentry.dsn,
            traces_sample_rate=config.sentry.traces_sample_rate,
        )
        logger.info('Sentry enabled')

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
