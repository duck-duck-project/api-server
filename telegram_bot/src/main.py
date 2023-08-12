import pathlib
from functools import partial

import aiohttp
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode
from aiohttp import ClientTimeout

import anonymous_messaging.handlers
import common.handlers
import whisper.handlers
from common.middlewares import DependencyInjectMiddleware
from config import load_config_from_file_path


def register_handlers(dispatcher: Dispatcher) -> None:
    common.handlers.register_handlers(dispatcher)
    whisper.handlers.register_handlers(dispatcher)

    # it's important to register anonymous_messaging.handlers after all handlers
    anonymous_messaging.handlers.register_handlers(dispatcher)


def main() -> None:
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config_from_file_path(config_file_path)

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
    )
    dispatcher.setup_middleware(dependency_inject_middleware)

    executor.start_polling(
        dispatcher=dispatcher,
        skip_updates=True,
    )


if __name__ == '__main__':
    main()
