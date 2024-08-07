from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from dotenv import load_dotenv

import os

load_dotenv()

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Регистрация')],
        [KeyboardButton(text='Вход')],
        [KeyboardButton(text='Смена пароля')]
    ],
    resize_keyboard=True
)

webapp = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Войти", web_app=WebAppInfo(url=os.getenv('WEB_URL')))]
    ]
)