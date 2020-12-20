from typing import List


class Repo:
    def __init__(self, conn):
        self.conn = conn

    # users
    async def list_users(self) -> List[int]:
        return [
            # row[0]
            # async for row in self.conn.execute(
            #     "select userid from tg_users",
            # )
        ]
