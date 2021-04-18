from dataclasses import dataclass


@dataclass
class TestUser:
    id: int
    name: str
    telegram_id: int
    status: int

    __select__ = '''select id, name, status, telegram_id from tel_user'''
