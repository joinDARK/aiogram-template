import asyncio
import os

from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from dotenv import load_dotenv

from bot.handlers import common
from logger import setup_logger

load_dotenv()


async def main() -> None:
    # Настройка логера
    logger = setup_logger(__name__)

    # Получаем токен бота. Также проверяем его наличие, иначе вызываем ошибку
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if BOT_TOKEN is None:
        logger.critical(
            f"Не задан токен бота в переменных окружения. BOT_TOKEN: {BOT_TOKEN}"
        )
        raise Exception(
            f"Не задан токен бота в переменных окружения. BOT_TOKEN: {BOT_TOKEN}"
        )

    # Инициализируем бота и диспатчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Привязываем к диспатчеру роутер
    dp.include_router(common.router)

    logger.info("Запуск телеграм-бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
