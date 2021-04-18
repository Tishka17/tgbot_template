from typing import List
from tgbot.models.temp_test import TestUser

class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # users
    async def add_user(self, data) -> None:
        """Store user in DB, ignore duplicates"""
        async with self.conn.cursor() as cur:
            await cur.execute(f'INSERT INTO tel_user (name, status, telegram_id) VALUES("{data["name"]}","{data["status"]}","{data["telegram_id"]}")')
            await self.conn.commit()
        return


    async def del_user(self, db_user_id) -> None:
        """Store user in DB, ignore duplicates"""
        async with self.conn.cursor() as cur:
            await cur.execute(f' DELETE FROM tel_user WHERE id = "{db_user_id}" ')
            await self.conn.commit()
        return


    async def list_users(self) -> List[TestUser]:
        sql = TestUser.__select__
        async with self.conn.cursor() as cur:
            await cur.execute(sql)
            return await cur.fetchall()
