from asyncio import get_event_loop

from aio_pika import Channel, RobustConnection, connect_robust
from aio_pika.pool import Pool
from app.settings import get_settings

settings = get_settings()


class RabbitMQWrapper:
    def __init__(self) -> None:
        self.healthz_name = "rabbitmq"
        self.connection_pool: Pool[RobustConnection]
        self.channel_pool: Pool[Channel]
        self.rabbitmq_dsn = settings.rabbitmq_dsn
        self.rabbitmq_connection_pool_max_size = settings.rabbitmq_connection_pool_max_size

    async def startup_event_handler(self) -> None:
        loop = get_event_loop()
        self.connection_pool = Pool(
            self._get_connection,
            max_size=self.rabbitmq_connection_pool_max_size,
            loop=loop,
        )
        self.channel_pool = Pool(
            self._get_channel,
            max_size=self.rabbitmq_connection_pool_max_size,
            loop=loop,
        )

    async def shutdown_event_handler(self) -> None:
        await self.channel_pool.close()
        await self.connection_pool.close()

    async def health_check(self) -> None:
        async with self.connection_pool.acquire() as connection:
            assert connection.is_closed is False

    async def _get_connection(self) -> RobustConnection:
        return await connect_robust(self.rabbitmq_dsn)

    async def _get_channel(self) -> Channel:
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()  # type: ignore
