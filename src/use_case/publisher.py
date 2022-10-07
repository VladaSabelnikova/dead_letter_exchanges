"""Модуль содержит демо функцию публикующую сообщение в очередь."""
import asyncio

from config.settings import config
from message_brokers.rabbit_message_broker import message_broker_factory


async def publisher() -> None:

    """Функция для быстрого знакомства с интерфейсом."""

    queue_name = 'queue_alive'  # Зададим произвольное имя очереди.
    await message_broker_factory.idempotency_startup()  # Разворачиваем DLX инфрастуктуру.

    # Публикуем несколько сообщений в очередь.
    for i in range(1, 6):
        message_body = f'message {i}'.encode()

        await message_broker_factory.publish(
            message_body=message_body,
            queue_name=queue_name,
            message_headers={'x-request-id': f'request-id-{i}'}
        )

    # Публикуем kill-signal, чтобы удалить очередь и закрыть consumer-а.
    await message_broker_factory.publish(
        message_body=config.rabbit.kill_signal,
        queue_name=queue_name
    )


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(publisher())
