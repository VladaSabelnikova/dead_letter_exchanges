# flake8: noqa
"""Модуль содержит асинхронную функцию backoff."""
from asyncio import sleep
from functools import wraps
from logging import getLogger
from typing import Union, Callable, Any

from utils.custom_exceptions import ConnectionTimeoutError


def timeout_limiter(
    max_timeout: Union[int, float],
    logger_name: str,
    start_sleep_time: Union[int, float] = 0.1,
    factor: Union[int, float] = 2,
) -> Callable:
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor).
    Вызывает исключение при достижении лимита таймаута.

    Args:
        max_timeout: предел ожидания ответа, после которого вызывается исключение
        logger_name: имя логгера
        start_sleep_time: начальное время повтора выполнения функции
        factor: во сколько раз нужно увеличить время ожидания

    Returns:
        Пробует выполнить функцию func и, если что-то пошло не так, «засыпает» на какое-то время.
    """

    def func_wrapper(func: Callable) -> Callable:

        """
        Декоратор может обрабатывать любую функцию, где возможны непредвиденные ошибки с подключением.

        Args:
            func: функция, которая подключается к базе

        Returns:
            Возвращает функцию, которая и выполняет алгоритм.
        """

        logger = getLogger(logger_name)

        @wraps(func)
        async def inner(*args: tuple, **kwargs: dict) -> Any:

            """
            Возвращаемая декоратором функция.
            При неудачном подключении к базе данных повторяет попытку через start_sleep_time.
            После превышения лимита ожидания вызывает исключение

            Args:
                *args: вся неименованная хрень, нужная для func
                **kwargs: вся именованная хрень, нужная для func

            Raises:
                Если ошибка critical — ждём восстановления сервиса,
                иначе продолжаем работу игнорируя исключение.

            Returns:
                Выполняет func пока она работает,
                если «что-то пошло не так» — повторяет попытку вызвать func через интервал start_sleep_time.
                Соответственно,
                чтобы меньше долбать базу без толку интервал увеличивается с каждым разом
            """

            nonlocal start_sleep_time  # Переменная точно не глобальная, но и не локальная вроде :)
            execution_time: float = 0

            while True:
                try:
                    return await func(*args, **kwargs)

                except Exception as error:

                    if execution_time < max_timeout:
                        logger.warning(f'waiting for {start_sleep_time} sec | {error}')
                        await sleep(start_sleep_time)
                        execution_time += start_sleep_time
                        start_sleep_time = min(start_sleep_time * factor, max_timeout - execution_time)
                    else:
                        raise ConnectionTimeoutError(
                            source_name=logger_name,
                            message='Connection timeout',
                            error_type=str(error),
                        )

        return inner

    return func_wrapper
