from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        db_session = obj.bot.get('db')
        # Передаем данные из таблицы в хендлер
        # data['some_model'] = await Model.get()
