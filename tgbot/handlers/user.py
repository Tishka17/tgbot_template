from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def user_start(m: Message, state: FSMContext):
    await m.reply("Hello, user!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
