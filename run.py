import asyncio
import logging

from aiogram import Dispatcher

from app.handlers import router
from bot import bot


logging.basicConfig(level=logging.INFO)

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Exit')