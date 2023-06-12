from app.libs.wrappers.rabbit_wrapper import RabbitMQWrapper
from app.settings import get_settings
import asyncio


settings = get_settings()

#
# class AsyncIterator:
#
#     def __init__(self):
#         self.counter = 0
#
#     def __aiter__(self):
#         return self
#
#     async def __anext__(self):
#         self.counter += 1
#         return self.counter


async def qwerty():
    while True:
        print(list_of_messages)
        if len(list_of_messages) > 0:
            message = list_of_messages[0]
            list_of_messages.remove(message)
            handler(message)
        await asyncio.sleep(5)





def handler(message):
    import time
    start_time = time.time()
    print('start')
    print(message)
    time.sleep(10)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('end')


list_of_messages = []

async def get_messages():
    rabbit_mq = RabbitMQWrapper()
    queue_name = settings.queue_name
    await rabbit_mq.startup_event_handler()
    async with rabbit_mq.channel_pool.acquire() as channel:
        queue = await channel.get_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    list_of_messages.append(message.body.decode())

    await rabbit_mq.shutdown_event_handler()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(get_messages(), qwerty()))
    # loop.run_until_complete(get_messages())
