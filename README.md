# Weather Telegram Bot
- Этот проект представляет собой Telegram-бота, который предоставляет информацию о текущей погоде в указанном городе, используя API OpenWeatherMap и библиотеку `python-telegram-bot`.

## Пример результата
- ![Screenshot_20250401_222848](https://github.com/user-attachments/assets/09d23a35-237f-4dd4-a440-951ebb261b12)

## Возможности
- Отвечает на команду `/start` приветственным сообщением.
- Предоставляет текущую погоду (температура, описание, влажность) по названию города.
- Работает асинхронно для стабильной обработки запросов.

## Требования
- Python 3.6+.
- Библиотеки: `python-telegram-bot` (версия 20.0+), `requests`.

## Установка
- Проверьте Python: `python3 --version`
- (Опционально) Создайте виртуальное окружение: `python3 -m venv venv`
- Активируйте его: `source venv/bin/activate` (для Linux/Mac) или `venv\Scripts\activate` (для Windows)
- Установите библиотеки: `pip3 install python-telegram-bot requests --upgrade`
- Скачайте `weather_bot.py`.
- Получите токен бота от [BotFather](https://t.me/BotFather) в Telegram и вставьте его в переменную `TOKEN` в коде.
- Получите API-ключ от [OpenWeatherMap](https://openweathermap.org/) и вставьте его в переменную `API_KEY` в коде.

## Использование
- Перейдите в папку с файлом: `cd путь_к_папке_с_файлом`
- Запустите скрипт: `python3 weather_bot.py`
- Откройте Telegram, найдите бота по имени пользователя и начните чат (например, с `/start`).
- Напишите название города (например, "Москва"), чтобы получить погоду.

## Структура проекта
- `weather_bot.py` — основной скрипт бота.
- `README.md` — описание проекта.
- `.gitignore` — файл для исключения ненужных файлов при загрузке в GitHub.
- `LICENSE` — лицензия проекта.

## Автор
- 1Mangust1981

## Лицензия
- MIT. Подробности в `LICENSE`.
