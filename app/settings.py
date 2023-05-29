import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    video_download_path: str

    rabbitmq_dsn: str
    rabbitmq_connection_pool_max_size: int = 4

    exchange_name: str
    queue_name: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_settings() -> Settings:
    settings = Settings()

    return settings
