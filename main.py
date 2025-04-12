import argparse
import asyncio
import logging

from aiogram import Bot, Dispatcher

from core.config import BOT_API_TOKEN, DATABASE_PATH
from core.logging import LoggerConfig
from data.factory import StorageFactory
from data.manager import DataManager
from handlers.base import setup_handlers


async def main(storage_type: str, db_path: str) -> None:
    bot = Bot(token=BOT_API_TOKEN)
    dp = Dispatcher()

    storage = StorageFactory.create_storage(
        storage_type,
        db_path=db_path,
    )
    data_manager = DataManager(storage)

    dp.include_router(setup_handlers(data_manager))

    logger.info(f"Бот запущен с типом хранилища: {storage_type}")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    logger = LoggerConfig(
        logger_name="main",
        log_file="cab.log",
        log_level=logging.DEBUG,
        console_output=True,
    ).get_logger()

    parser = argparse.ArgumentParser(description="Crypto Assistant Bot")
    parser.add_argument(
        "-s",
        "--storage",
        type=str,
        default="sqlite",
        choices=["memory", "sqlite", "json"],
        help="Тип хранилища: memory, sqlite или json (по умолчанию: sqlite)",
    )
    args = parser.parse_args()

    asyncio.run(main(args.storage, DATABASE_PATH))
