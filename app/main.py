import time

from app.libs.wrappers.rabbit_wrapper import RabbitMQWrapper
from app.settings import get_settings
import asyncio
from multiprocessing import Process, Manager

settings = get_settings()

def qwerty(list_of_messages):

    while True:

        print(f'функция qwerty печатает {list_of_messages}')
        if len(list_of_messages) > 0:
            message = list_of_messages[0]
            list_of_messages.remove(message)
            handler(message)
        time.sleep(5)

def handler(message):
    import time
    start_time = time.time()
    print('start')
    print(message)
    time.sleep(600)
    print("--- %s seconds ---" % (time.time() - start_time))
    print('end')


async def get_messages(list_of_messages):

    rabbit_mq = RabbitMQWrapper()
    queue_name = settings.queue_name
    await rabbit_mq.startup_event_handler()
    async with rabbit_mq.channel_pool.acquire() as channel:
        queue = await channel.get_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    list_of_messages.append(message.body.decode())
                    print(f'добавилось видео {message.body.decode()}')
                    print(f'функция get_messages печатает {list_of_messages}')

    await rabbit_mq.shutdown_event_handler()

def huy(list_of_messages):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_messages(list_of_messages))

def main():
    manager = Manager()
    list_of_messages = manager.list()
    qwerty_p = Process(target=qwerty, args=(list_of_messages,))
    huy_p = Process(target=huy, args=(list_of_messages,))
    qwerty_p.start()
    huy_p.start()
    qwerty_p.join()
    huy_p.join()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_messages())
