from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select
from dotenv import load_dotenv

from app.keyboards import main, webapp



class Registration(StatesGroup):
    password = State()

class Reset(StatesGroup):
    password = State()


load_dotenv()
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет, это бот для входа в BookIs !", reply_markup=main)


@router.message(F.text.lower() == 'регистрация')
async def start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    async with async_session() as session:
        id = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not id:
            await message.answer('Введите ваш пароль:')
            await state.set_state(Registration.password)
        else:
            await message.answer(f'Вы уже зарегистрированы !', reply_markup=main)
            await state.clear()

@router.message(Registration.password)
async def register2(message: Message, state: FSMContext):
    password = message.text
    tg_id = message.from_user.id
    async with async_session() as session:
        id = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not id:
            session.add(User(tg_id=tg_id, password=password))
            await session.commit()
            await message.answer('Вы успешно зарегистрированы ! 🎉', reply_markup=main)
            await state.clear()
        if id:
            await message.answer("Вы уже зарнгистрированы !", reply_markup=main)
            await state.clear()

@router.message(F.text.lower() == 'смена пароля')
async def start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    async with async_session() as session:
        id = await session.scalar(select(User).where(User.tg_id == tg_id))
        if id:
            await message.answer('Введите новый пароль :')
            await state.set_state(Reset.password)
        elif not id:
            await message.answer('Вы не зарегистрированны !', reply_markup=main)
            await state.clear()

@router.message(Reset.password)
async def register2(message: Message, state: FSMContext):
    password = message.text
    tg_id = message.from_user.id
    async with async_session() as session:
        id = await session.scalar(select(User).where(User.tg_id == tg_id))
        if id:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.password = password
            await session.commit()
            await message.delete()
            await message.answer('Пароль успешно изменен.', reply_markup=main)
            await state.clear()

@router.message(F.text.lower() == 'вход')
async def start(message: Message):
    tg_id = message.from_user.id
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        await message.answer(f'Логин: <code>{tg_id}</code>\n'
                             f'Пароль: <tg-spoiler>{user.password}</tg-spoiler>\n'
                             f'Вход в приложение',
                             reply_markup=webapp,
                             parse_mode=ParseMode.HTML)


@router.message()
async def echo(messange: Message):
    await messange.answer('Я вас не понимаю. Используйте встроенные команды', reply_markup=main)