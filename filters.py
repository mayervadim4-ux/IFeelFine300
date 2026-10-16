"""Кастомные фильтры."""

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdmin(BaseFilter):
    def __init__(self, admins: list[int]) -> None:
        self.admins = set(admins)

    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and message.from_user.id in self.admins
