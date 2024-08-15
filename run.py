from app.database.models import async_main
from app.handlers import router
from threading import Thread

from Flask_app.init import app

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import asyncio, os

load_dotenv()



async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def run_flask():
    app.run(port=5000)


if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    #logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass