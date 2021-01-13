from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # users
    async def add_user(self, user_id) -> None:
        """Store user in DB, ignore duplicates"""
        # await self.conn.execute(
        #     "INSERT INTO tg_users(userid) VALUES $1 ON CONFLICT DO NOTHING",
        #     user_id,
        # )
        return

    async def list_users(self) -> List[int]:
        """List all bot users"""
        return [
            # row[0]
            # async for row in self.conn.execute(
            #     "select userid from tg_users",
            # )
        ]
