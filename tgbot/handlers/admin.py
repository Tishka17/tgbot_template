from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo


# States
class DialogS(StatesGroup):
    s1 = State()
    s2 = State()

async def admin_start(m: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_mode'] = False
    await DialogS.s1.set()
    await m.reply("Hello, admin!")


async def show_current_state(message: Message, state: FSMContext):
    currentState = await state.get_state()
    await message.reply(f'Текущее состояние: {currentState}')


async def goto_next_state(message: Message, state: FSMContext):
    currentState = await state.get_state()
    await message.reply(f'Прошлое состояние: {currentState}')
    await DialogS.next()
    currentState = await state.get_state()
    await message.reply(f'Текущее состояние: {currentState}')

async def echo1(message: Message):
    user = message.from_user
    await message.answer(f'Привет, {user.first_name} {user.last_name}! (@{user.username}, id: {user.id})')
    await message.answer('Для того чтобы ввести начать работу нажмите /start')
    if message.forward_from :
        await message.answer(f'Переслано от user.id: {message.forward_from.id}')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"])
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(show_current_state, state="*", commands=["state"])
    dp.register_message_handler(goto_next_state, state="*", text=["next"])
    dp.register_message_handler(echo1,  is_admin=True)
