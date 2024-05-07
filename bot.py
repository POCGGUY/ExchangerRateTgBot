import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from app.handlers import router

logging.basicConfig(level=logging.INFO)
bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher()
dp.include_router(router)

async def botStart():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()