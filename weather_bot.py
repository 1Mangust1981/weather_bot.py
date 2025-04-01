import logging
# Импортируем модуль логирования для отслеживания событий и ошибок.
# Логирование полезно для отладки и мониторинга работы бота.
# Логи будут записываться с уровнем INFO и выше.

import requests
# Импортируем библиотеку requests для выполнения HTTP-запросов.
# Она нужна для обращения к API OpenWeatherMap.
# Позволяет получать данные о погоде в формате JSON.

from telegram import Update
# Импортируем класс Update из библиотеки telegram.
# Он нужен для обработки входящих обновлений,
# таких как сообщения или команды от пользователей.

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
# Импортируем необходимые классы из telegram.ext.
# ApplicationBuilder создает приложение бота,
# CommandHandler обрабатывает команды, MessageHandler — сообщения,
# filters фильтрует типы сообщений, ContextTypes — для асинхронности.

# Настраиваем базовое логирование для вывода информации
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
# Устанавливаем формат логов с временем, именем и уровнем.
# Уровень INFO позволяет видеть основные события.
# Логи будут полезны для проверки работы бота.

# Убираем лишние логи от httpx, чтобы терминал не захламлялся
logging.getLogger("httpx").setLevel(logging.WARNING)
# Устанавливаем уровень WARNING для httpx,
# чтобы не видеть все запросы GET и POST.
# Это делает вывод в терминале чище.
logger = logging.getLogger(__name__)
# Создаем логгер с именем текущего модуля для отладки.

# Задаем токен бота и API-ключ OpenWeatherMap
TOKEN = "your_bot_token_here"
# Токен для связи бота с Telegram.
# Замените "your_bot_token_here" на токен от BotFather.
# Храните токен в безопасном месте, не публикуйте публично.
API_KEY = "your_openweathermap_api_key_here"
# API-ключ для OpenWeatherMap.
# Замените "your_openweathermap_api_key_here" на ваш ключ.
# Храните ключ в безопасном месте, не публикуйте публично.

# Определяем функцию для получения погоды по названию города
def get_weather(city: str) -> str:
    # Функция запрашивает погоду для указанного города.
    # Использует API OpenWeatherMap для получения данных.
    # Возвращает строку с информацией о погоде.
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    # Базовый URL для API OpenWeatherMap.
    # Используется для текущей погоды (endpoint /weather).
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    # Параметры запроса: город, API-ключ, единицы измерения (градусы Цельсия),
    # язык (русский для описания погоды).
    try:
        response = requests.get(base_url, params=params)
        # Выполняем GET-запрос к API с указанными параметрами.
        # Получаем ответ в формате JSON.
        response.raise_for_status()
        # Проверяем, успешен ли запрос (код 200).
        # Если нет, вызовется исключение.
        data = response.json()
        # Преобразуем ответ в словарь Python.
        # Данные содержат информацию о погоде.
        temp = data["main"]["temp"]
        # Извлекаем температуру в градусах Цельсия.
        description = data["weather"][0]["description"]
        # Извлекаем описание погоды (например, "ясно").
        humidity = data["main"]["humidity"]
        # Извлекаем влажность в процентах.
        return (
            f"Погода в {city}:\n"
            f"Температура: {temp}°C\n"
            f"Описание: {description.capitalize()}\n"
            f"Влажность: {humidity}%"
        )
        # Формируем строку с данными о погоде.
        # Возвращаем её для отправки пользователю.
    except requests.exceptions.RequestException as e:
        # Обрабатываем ошибки запроса (например, город не найден).
        logger.error(f"Ошибка при запросе погоды: {e}")
        # Логируем ошибку для отладки.
        return "Не удалось получить погоду. Проверьте название города."
        # Возвращаем сообщение об ошибке.

# Определяем функцию для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Функция отправляет приветственное сообщение при команде /start.
    # Асинхронная, так как использует await для отправки.
    await update.message.reply_text(
        "Привет! Я бот погоды. Напиши название города, "
        "и я расскажу о погоде!"
    )
    # Отправляем пользователю текстовый ответ.
    # Сообщение объясняет, как пользоваться ботом.

# Определяем функцию для обработки текстовых сообщений (названий городов)
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Функция обрабатывает текстовые сообщения от пользователя.
    # Ожидает название города и возвращает погоду.
    city = update.message.text
    # Получаем текст сообщения (название города).
    logger.info(f"Получен запрос погоды для города: {city}")
    # Логируем запрос для отладки.
    weather_info = get_weather(city)
    # Вызываем функцию get_weather для получения погоды.
    await update.message.reply_text(weather_info)
    # Асинхронно отправляем пользователю информацию о погоде.

# Создаем приложение бота с использованием токена
application = ApplicationBuilder().token(TOKEN).build()
# ApplicationBuilder создает экземпляр бота.
# Метод token() принимает токен для аутентификации.
# Метод build() завершает настройку приложения.

# Добавляем обработчик для команды /start
application.add_handler(CommandHandler("start", start))
# CommandHandler связывает команду /start с функцией start.
# Это позволяет боту реагировать на команду.

# Добавляем обработчик для текстовых сообщений
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))
# MessageHandler обрабатывает текстовые сообщения.
# Фильтр TEXT & ~COMMAND исключает команды вроде /start.
# Это предотвращает обработку команд как названий городов.
# Связываем его с функцией weather.

# Запускаем бота в режиме опроса (polling)
application.run_polling()
# Метод run_polling() запускает бесконечный цикл.
# Бот будет получать обновления от Telegram.
# Остановить можно с помощью Ctrl+C в терминале.
