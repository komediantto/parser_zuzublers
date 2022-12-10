from aiogram import executor

from BotDB import db
from create_bot import dp
from handlers import main_handler


async def start(_):
    print('Бот запущен')
    db.sql_start()


main_handler.register(dp)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True, on_startup=start)
