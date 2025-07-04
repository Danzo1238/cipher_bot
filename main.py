import os
import asyncio
import logging

from handlers.caesar import caesar_cipher, dccaesar
from handlers.vernam import dcvernam, vernam
from handlers.emoji import dcemoji, emoji_cipher
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import start

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(caesar_cipher.router)
    dp.include_router(start.router)
    dp.include_router(dccaesar.router)
    dp.include_router(vernam.router)
    dp.include_router(dcvernam.router)
    dp.include_router(emoji_cipher.router)
    dp.include_router(dcemoji.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")



