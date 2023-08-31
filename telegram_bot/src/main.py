import pathlib
from functools import partial

import aiohttp
import humanize
import sentry_sdk
import structlog
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode
from aiohttp import ClientTimeout
from structlog.stdlib import BoundLogger

import handlers
from config import load_config_from_file_path
from logger import setup_logging
from middlewares import (
    DependencyInjectMiddleware,
    UserMiddleware,
    BannedUsersFilterMiddleware,
)

logger: BoundLogger = structlog.get_logger('app')


def register_handlers(dispatcher: Dispatcher) -> None:
    handlers.register_handlers(dispatcher)
    logger.info('Handlers registered')


def main() -> None:
    humanize.i18n.activate('ru_RU')

    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config_from_file_path(config_file_path)

    setup_logging(config.logging.level)

    bot = Bot(token=config.telegram_bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(
        bot=bot,
        storage=RedisStorage2(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
        ),
    )

    register_handlers(dispatcher)

    dependency_inject_middleware = DependencyInjectMiddleware(
        bot=bot,
        dispatcher=dispatcher,
        closing_http_client_factory=partial(
            aiohttp.ClientSession,
            base_url=config.server_api_base_url,
            timeout=ClientTimeout(60),
        ),
        chat_id_for_retranslation=config.main_chat_id,
        timezone=config.timezone,
    )
    dispatcher.setup_middleware(dependency_inject_middleware)
    dispatcher.setup_middleware(UserMiddleware())
    dispatcher.setup_middleware(BannedUsersFilterMiddleware())

    if config.sentry.is_enabled:
        sentry_sdk.init(
            dsn=config.sentry.dsn,
            traces_sample_rate=config.sentry.traces_sample_rate,
        )
        logger.info('Sentry enabled')

    executor.start_polling(
        dispatcher=dispatcher,
        skip_updates=True,
    )


if __name__ == '__main__':
    main()
