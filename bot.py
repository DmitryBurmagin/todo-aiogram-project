import asyncio

from config_reader import config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from handlers import cmd


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())

    storage = RedisStorage.from_url('redis://localhost:6379/0')

    dp = Dispatcher(storage=storage)

    dp.include_routers(cmd.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
