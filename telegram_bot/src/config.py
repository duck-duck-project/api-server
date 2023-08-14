import pathlib
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass

__all__ = (
    'RedisConfig',
    'SentryConfig',
    'Config',
    'load_config_from_file_path',
    'parse_config',
)


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: str
    port: int
    db: int


@dataclass(frozen=True, slots=True)
class SentryConfig:
    dsn: str
    traces_sample_rate: float


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    redis: RedisConfig
    sentry: SentryConfig
    server_api_base_url: str
    main_chat_id: int | str


def parse_config(config: Mapping) -> Config:
    return Config(
        telegram_bot_token=config['telegram_bot']['token'],
        redis=RedisConfig(
            host=config['redis']['host'],
            port=config['redis']['port'],
            db=config['redis']['db'],
        ),
        sentry=SentryConfig(
            dsn=config['sentry']['dsn'],
            traces_sample_rate=config['sentry']['traces_sample_rate'],
        ),
        server_api_base_url=config['server_api']['base_url'],
        main_chat_id=config['main_chat_id'],
    )


def load_config_from_file_path(file_path: pathlib.Path) -> Config:
    config_text = file_path.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)
    return parse_config(config)
