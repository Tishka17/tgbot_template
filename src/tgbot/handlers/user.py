from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.services.repository import Repo
from tgbot.states.user import UserMain


async def user_start(m: Message, repo: Repo, state: FSMContext):
    await repo.add_user(m.from_user.id)
    await m.reply("Hello, user!")
    await state.set_state(UserMain.SOME_STATE)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
