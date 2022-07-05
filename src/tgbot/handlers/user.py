from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.repository import Repo


async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id)
    await m.reply("Hello, user!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
