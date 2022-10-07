"""Модуль содержит функцию публикующую сообщение в очередь."""
import asyncio
from asyncio import sleep

from message_brokers.rabbit_message_broker import message_broker_factory


async def publisher() -> None:

    """Функция для быстрого знакомства с интерфейсом."""

    queue_name = 'queue_alive'
    await message_broker_factory.idempotency_startup()

    for i in range(1, 6):
        message_body = f'message {i}'.encode()

        await message_broker_factory.publish(
            message_body=message_body,
            queue_name=queue_name,
            message_headers={'x-request-id': f'request-id-{i}'}
        )

        await sleep(1)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(publisher())
