from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('⬆️Загрузить файл')
    keyboard.row(b1)
    return keyboard
