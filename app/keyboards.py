from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from dotenv import load_dotenv
from pyngrok import ngrok

import os

load_dotenv()

# ___config_ngrok___ make ngrok link
ngrok.set_auth_token(os.getenv('NGROK_AUTHTOKEN'))
public_url = ngrok.connect(8080).public_url
print(public_url)


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
        [InlineKeyboardButton(text="Войти", web_app=WebAppInfo(url=public_url))]
    ]
)