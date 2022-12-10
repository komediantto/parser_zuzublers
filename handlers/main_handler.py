from aiogram import Dispatcher, types
import keyboards.main_keyboard as kb
from aiogram.dispatcher.filters import Text
from BotDB import db
import pandas as pd
from aiogram.types import ReplyKeyboardRemove


async def start(message: types.Message):
    await message.answer('Привет, я бот для парсинга. Начнём?',
                         reply_markup=kb.main_keyboard())


async def ask_file(message: types.Message):
    await message.answer('Прикрепите файл в формате .xlsx',
                         reply_markup=ReplyKeyboardRemove())


async def take_file(message: types.Message):
    print('Скачиваю файл..')
    await message.document.download('file.xlsx')
    print('Успешно')
    df = pd.read_excel('file.xlsx')
    await message.answer(df.head(10))
    await db.sql_add_command()
    await message.answer(
        f'Нужно немного подождать, время ожидания ~ {len(df)*15} секунд')
    avg = await db.lets_some_parse(df)
    for price in avg:
        await message.answer(f'Средняя стоимость товара -> {price}',
                             reply_markup=kb.main_keyboard())


def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start',])
    dp.register_message_handler(ask_file, Text(equals='⬆️Загрузить файл'))
    dp.register_message_handler(take_file,
                                content_types=types.ContentType.DOCUMENT)
