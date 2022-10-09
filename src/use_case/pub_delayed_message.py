"""Модуль содержит демо функцию, публикующую отложенное сообщение в очередь."""
import asyncio

from src.message_brokers.rabbit_message_broker import message_broker_factory


async def publisher() -> None:

    """Функция для быстрого знакомства с интерфейсом."""

    queue_name = 'queue_alive'  # Зададим произвольное имя очереди.
    await message_broker_factory.idempotency_startup()  # Разворачиваем DLX инфрастуктуру.

    # Публикуем отложенное на 10 секунд сообщение.
    await message_broker_factory.publish(
        message_body=b'delayed message',
        queue_name=queue_name,
        message_headers={'x-request-id': 'delayed message number one'},
        delay=10
    )


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(publisher())
