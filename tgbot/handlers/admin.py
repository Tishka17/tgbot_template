from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import Message, ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
import aiogram.utils.markdown as md

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo


# States
class AddUserDialog(StatesGroup):
    get_forwarded_message = State()
    set_status = State()
    submit = State()

class DelUserDialog(StatesGroup):
    set_id = State()
    submit = State()

def get_int(str):
    try:
        r = int(str)
        return r
    except ValueError:
        return 0


async def do_cancel(m: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await m.answer("Процедура ввода пользователя прервана...Удачи!", reply_markup=ReplyKeyboardRemove())


async def show_current_state(m: Message, state: FSMContext):
    currentState = await state.get_state()
    await m.reply(f'Текущее состояние диалога: {currentState}')


async def adduser_start(m: Message, state: FSMContext):
    await AddUserDialog.get_forwarded_message.set()
    await m.answer("Для добавления пользователя в базу перешлите мне сообщение от него. Если в нем не будет поля 'forward_from' ... то я пока не знаю, что делать...")


async def process_forwarded_message(m: Message, state: FSMContext):
    if not m.forward_from :
        await m.answer("ПОВТОРЯЮ! Для добавления пользователя в базу перешлите мне сообщение от него. Если в нем нет поля 'forward_from' ... то я не знаю, что делать...")
        return

    await AddUserDialog.next()
    async with state.proxy() as data:
        data['telegram_id'] = m.forward_from.id
        data['name'] = m.forward_from.username
    await m.answer(f'Ok. Сообщение переслано от пользователя с id: {m.forward_from.id}')
    await m.answer("Введите статус пользователя (любое число)")


async def process_set_status(m: Message, state: FSMContext):
    await AddUserDialog.next()
    async with state.proxy() as data:
        data['status'] = get_int(m.text)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.insert('Подтверждаю')
    markup.insert('Отменить')
    await m.reply(f'Ok. Установлен статус: {data["status"]}')
    await m.answer('Подтвердите введенные данные', reply_markup=markup)
    await sendCollectedData(m, data, state)


async def sendCollectedData(m: Message, data, state):
    return await m.answer(
        f'''Telegram user_id: {data["telegram_id"]}
Username: `{data["name"]}`
Статус: {data["status"]}
        ''' )

async def process_submit(m: Message, state: FSMContext, repo: Repo):
    if m.text == 'Подтверждаю' :
        async with state.proxy() as data:
            await repo.add_user(data)
        mes_text = 'Пользователь добавлен в базу:'
    else:
        mes_text = 'Пользователь НЕ добавлен в базу'

    await m.answer(mes_text, reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def any_message(m: Message):
    user = m.from_user
    await m.answer(f'Привет, админ! {user.first_name} {user.last_name}! (@{user.username}, id: {user.id})')
    await m.answer('''/adduser - добавить пользователя в БД
/showuser - посмотреть список пользователей
/deluser - удалить пользователя из БД
/state - текущее состояние диалога от FSM
cancel - прервать текущую процедуру (диалог)'''
    )


async def showuser(m: Message, repo: Repo):
    some_thing = await repo.list_users()
    await m.answer(f'Список пользователей: {some_thing[0:]}')

async def deluser_start(m: Message, state: FSMContext):
    await DelUserDialog.set_id.set()
    await m.answer("Для удаления пользователя из базы напишите мне его id")

async def deluser_set_id(m: Message, state: FSMContext):
    try:
        userid = int(m.text)
    except ValueError:
        await m.reply(f'Надо ввести число')
        return False

    await DelUserDialog.next()
    async with state.proxy() as data:
        data['userid'] = userid

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Подтверждаю','Отменить')
    await m.reply(f'Ok. Вы собираетесь удалить пользователя с id: {data["userid"]}')
    await m.answer('Подтвердите удаление', reply_markup=markup)


async def deluser_submit(m: Message, state: FSMContext, repo: Repo):
    if m.text == 'Подтверждаю' :
        async with state.proxy() as data:
            await repo.del_user(data['userid'])
        mes_text = 'Пользователь удален'
    else:
        mes_text = 'Пользователь НЕ удален'

    await m.answer(mes_text, reply_markup=ReplyKeyboardRemove())
    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(any_message, commands=["start"], is_admin=True)
    dp.register_message_handler(adduser_start, commands=["adduser"], is_admin=True)
    dp.register_message_handler(showuser, commands=["showuser"], is_admin=True)
    dp.register_message_handler(deluser_start, commands=["deluser"], is_admin=True)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(do_cancel, text=["cancel"], state="*", is_admin=True)
    dp.register_message_handler(show_current_state, state="*", commands=["state"], is_admin=True)
    dp.register_message_handler(process_forwarded_message, state=AddUserDialog.get_forwarded_message, is_admin=True)
    dp.register_message_handler(process_set_status, state=AddUserDialog.set_status, is_admin=True)
    dp.register_message_handler(process_submit, state=AddUserDialog.submit, is_admin=True)
    dp.register_message_handler(deluser_set_id, state=DelUserDialog.set_id, is_admin=True)
    dp.register_message_handler(deluser_submit, state=DelUserDialog.submit, is_admin=True)
    dp.register_message_handler(any_message, is_admin=True)
