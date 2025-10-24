import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from .logging_conf import setup_logging
from .settings import BOT_TOKEN
from .db.models import init_db
from .handlers import feedback, admin, errors
from .middlewares.throttling import Throttling
from .middlewares.acl import AdminACL

async def main():
    setup_logging()
    init_db()
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.update.middleware(Throttling())
    dp.update.middleware(AdminACL())

    dp.include_router(feedback.router)
    dp.include_router(admin.router)
    dp.include_router(errors.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
