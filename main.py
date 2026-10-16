"""Точка входа. Запуск: python main.py"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import handlers
from config import config
from db import Database

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="help", description="Помощь"),
            BotCommand(command="cancel", description="Отменить действие"),
        ]
    )


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
    )

    db = Database(config.db_path)
    await db.init()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    # Для продакшена замени на RedisStorage, иначе состояния теряются при рестарте.
    dp = Dispatcher(storage=MemoryStorage())
    # db прокидывается во все хендлеры как аргумент `db`.
    dp["db"] = db
    dp.include_router(handlers.get_router())

    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    me = await bot.get_me()
    logger.info("Бот запущен: @%s", me.username)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Остановлено пользователем")
