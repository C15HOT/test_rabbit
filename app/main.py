from app.libs.wrappers.rabbit_wrapper import RabbitMQWrapper
from app.settings import get_settings
import asyncio


settings = get_settings()


def handler():
    import time
    start_time = time.time()
    result = 99999999**999999
    print("--- %s seconds ---" % (time.time() - start_time))


async def get_messages():
    rabbit_mq = RabbitMQWrapper()
    queue_name = settings.queue_name
    await rabbit_mq.startup_event_handler()
    async with rabbit_mq.channel_pool.acquire() as channel:
        queue = await channel.get_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    handler()
                    print(message.body.decode())

    await rabbit_mq.shutdown_event_handler()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_messages())
