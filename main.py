import asyncio
from Token import TOKEN
from aiogram import Bot, Dispatcher
from database.models import async_main
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
from handlers import start_handlers, group_handlers
from apscheduler.schedulers.asyncio import AsyncIOScheduler

admin_id = '816427281'


async def main():
    await async_main()

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(start_handlers.message_push_user, trigger="interval", seconds=5)
    scheduler.start()

    dp = Dispatcher()
    dp.include_router(start_handlers.router)
    dp.include_router(group_handlers.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())