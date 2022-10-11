## Асинхронный интерфейс для RabbitMQ with DLX


### DLX use cases:
1. Контролируемый повтор сообщения в случае коллизий consumer-а
2. Отложенные сообщения
3. Сообщения по расписанию (scheduler)

### Интерфейс позволяет:
1. Автоматически развёртывать DLX инфрастуктуру
2. Автоматически создавать очереди в момент чтения или записи сообщения
3. Удалять очереди и завершать работу consumer-ов при помощи kill-signal
4. Асинхронно обрабатывать сообщения из очереди

**ВАЖНО:** Обращение к RabbitMQ по сети обёрнуто в backoff с лимитом таймаута

При помощи механизма DLX интерфейс реализует следующий функционал:
1. Единая точка входа всех сообщений с возможностью установки delay (отложенная обработка сообщений)
2. Повторная обработка сообщений в случае коллизий с ограничением числа повторов

   ![architecture_rabbit_mq](http://www.plantuml.com/plantuml/png/Z9BHIiCm58RlynIXFe2kKrPXY5jjmJl1Mw6SfMTTM9hC9DqSqdUtwzAPpgsOG6Z_ytz_mk4y6mlQLgKWKsFt0fy8RTO6s1eAfD-4khLeb4AhIkPC2QNfJHp7f-Bx2dAruxAWerQhspDNh2fHsg6Kn_l3zg2bXdBmtYH9_3l0mWBC835xY9FqpeC-Awm6YNGIfL7g4S2iqXuXk4IxucmjqHWwxkak8vmVjf-XjTfTpGZ_bR5K8aSz-FGqVfcCFOI1pWUxCqdcKUI0wQqR0j9D00YHWU1RpFokjT_7qrL750mDUahWpFKL9Fo3XBz8JNnW1zmsuvNbk05jFQvVEE0rkKXgj7hlWxxkkBPL-CLM80lCk6IgR2mjrAaVifClCaPfY_gCE8eN_TshVBl_8YXGMWeRtdfcRw-1ampgBMTTsqz_v-MmLmu3GgIoI1VAMbLIzTDd5Ums3GJHkxzYFw2k1CTAHOZVe1nGuz92SL6QId1B78M0AAqgmOK35N16Sfo4k8cp-ONPN-1BU6-oDRLZKAJ8cTrzy-RDctKEwks5-FBJ9P8RiMueKzULgKpuS-JwCd5zbs2BwucL6UAfP9Awn9sxdhj4c0SGol6KIY4vuIQoq3N4BLO6HfQ0-YMJ88fRXdGygVRHiyCEE3KrZa0_ZFi8QbPkwkJms2CB8olGwMhkAG9T77iTliHuGPMmqpacp7Sipu4oDP8fGa5w2KkxKoLO0ceWbWcmwkkp-8pSUvnQ8dov1K22aPRhkWy4NUABA4YpGBH7MZn4MYFTcYhN_PFu5DTZEtJzEqgmrU5nTD097smwSSV8jLZ2GhzyWu-MLD76dU_5vQ-PYRL5CjyEDg3Bf4rZ5JGEOVYuzVJqC6ezENk5S_KH0DSl83Uc4CQtWBh05PI2_TcBnOAtLQrbfU6CRk6YAYuP6LFQH8zPoL1iBlCWgESBmG8qglSBI7ohzwo2Y5PVh7E1p4ei5nTKZWjwfd1zewqSynIzmD0EnlJaJDLu4Rqnkxi-SOoNLnEr6hDxGL3v-GyjlVShDVrtAml-p1BeZY5T6VBBi3JtZiRn_amu12WvBste5teonzAC5HkyLu_sj_4UCB-xdx1v3e0Kqbn9OJZDvG1HMZQI00EsaKgJ11KCQXH1kcd0WuRWtrh3iDbYrsIHS_hXcQ5lyKLrwC6yCX8iacGp69FpM3eFlRrrgahZtj9g44BrAF2uT5ThjsnZmrSSpRnL-UH5AAyYzUlONqU5PvbY8Bt54E56Wkib8ekGga9ShYZVL2dSA1kPLXgBYrKJh3oC9xu5_BwIcH2AqmJBSmBqzlJmk0i01NRuQ9uDF-BlN0p9onUBYis4897Zr98E8T1wYjRZ_EZMC5jc_HZZcUIvrOVQqVDelrFrz4Qw-q5GPkRuD5s6vGuSRrn_Y5iL_sl_0000)




### Инструкция по развёртыванию:

1. Клонировать проект
2. Установить зависимости `poetry install`
3. Запустить RabbitMQ `docker-compose up -d`
4. В src/use_case добавить .env файл (образец в src/use_case/.env_example)

После этого можно запустить демонстрационные файлы:
* src/use_case/consumer.py (демонстрирует работу consumer-а)
* src/use_case/pub_casual_message.py (демонстрирует публикацию обычных сообщений)
* src/use_case/pub_delayed_message.py (демонстрирует публикацию отложенных сообщений)
* src/use_case/pub_kill_signal_message.py (демонстрирует публикацию kill-signal)


### Планы по доработке:
1. Усовершенствовать механизм выключения consumer-ов. Сейчас kill_signal может выключить только ОДИН consumer.
Это удобно для разовых очередей (например для работы с WebSocket).
Нужно доработать механизм для выключения ВСЕХ имеющихся consumer-ов у очереди (их может быть много).
