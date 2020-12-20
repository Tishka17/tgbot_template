from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.services.repository import Repo


class RoleMiddleware(LifetimeControllerMiddleware):
    def __init__(self, admin_id: int):
        super().__init__()
        self.admin_id = admin_id

    async def pre_process(self, obj, data, *args):
        data["is_admin"] = obj.from_user.id == self.admin_id

    async def post_process(self, obj, data, *args):
        del data["is_admin"]
