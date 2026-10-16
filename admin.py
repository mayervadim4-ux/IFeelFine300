"""Админские команды. Доступны только ID из ADMINS в .env."""

from aiogram import Router
from aiogram.filters import Command

from aiogram.types import Message

from config import config
from db import Database
from filters import IsAdmin

router = Router(name="admin")
# Фильтр на весь роутер — внутрь попадают только админы.
router.message.filter(IsAdmin(config.admins))


@router.message(Command("stats"))
async def cmd_stats(message: Message, db: Database) -> None:
    users, requests = await db.stats()
    await message.answer(f"📊 Пользователей: {users}\nЗаявок: {requests}")


@router.message(Command("ping"))
async def cmd_ping(message: Message) -> None:
    await message.answer("pong")
