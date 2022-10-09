"""Модуль содержит демо функцию читающую сообщения из очереди."""
import asyncio

from aio_pika.abc import AbstractIncomingMessage

from src.message_brokers.rabbit_message_broker import message_broker_factory


async def callback(message: AbstractIncomingMessage) -> None:

    """
    Функция для обработки каждого сообщения из очереди.
    В реальной работе можно и нужно изменить её под решаемую задачу.

    Обратите внимание, что нужно вручную управлять состоянием сообщения пользуясь ack, reject и т.д.
    Подробнее см.
    https://www.rabbitmq.com/confirms.html

    Так же следует следить за кол-вом повторных вставок сообщения в очередь,
    чтобы не зациклить повторную вставку сообщения в очередь и не замусорить её.
    Пример кода:

    code:
        if message.info()['headers']['x-death'][0]['count'] + 1 > config.rabbit.max_retry_count:
            await message.ack()


    Args:
        message: сообщение из очереди
    """

    print(message.body)  # noqa: WPS421
    await message.ack()


async def consumer() -> None:

    """Функция для быстрого знакомства с интерфейсом."""

    queue_name = 'queue_alive'  # Зададим произвольное название очереди.
    await message_broker_factory.idempotency_startup()  # Разворачиваем DLX инфрастуктуру.
    await message_broker_factory.consume(queue_name=queue_name, callback=callback)  # Ждём сообщений.


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(consumer())
