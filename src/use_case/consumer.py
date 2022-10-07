"""Модуль содержит функцию выкусывающую сообщения из очереди."""
import asyncio

from aio_pika.abc import AbstractIncomingMessage

from message_brokers.rabbit_message_broker import message_broker_factory


async def callback(message: AbstractIncomingMessage) -> None:

    """
    Функция для обработки каждого выкусанного сообщения из очереди.
    В реальной работе можно и нужно изменить её под решаемую задачу.

    Обратите внимание, что нужно вручную управлять состоянием сообщения пользуясь ack, reject и т.д.
    Подробнее см.
    https://www.rabbitmq.com/confirms.html

    Так же следует следить за кол-вом повторных вставок сообщения в очередь:

    code:
        if message.info()['headers']['x-death'][0]['count'] + 1 > config.rabbit.max_retry_count:
            await message.ack()

    что бы не зациклить повторную вставку сообщения в очередь и не замусорить её.

    Args:
        message: сообщение из очереди
    """

    print(message.body)  # noqa: WPS421
    await message.ack()


async def consumer() -> None:

    """Функция для быстрого знакомства с интерфейсом."""

    queue_name = 'queue_alive'
    await message_broker_factory.idempotency_startup()
    await message_broker_factory.consume(queue_name=queue_name, callback=callback)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(consumer())
