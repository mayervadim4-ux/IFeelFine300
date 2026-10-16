"""Базовые команды: /start, /help, профиль, о боте, фолбэк."""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from db import Database
from keyboards import main_menu

router = Router(name="common")

HELP_TEXT = (
    "Что я умею:\n"
    "/start — перезапустить бота\n"
    "/help — эта справка\n"
    "/cancel — отменить текущее действие\n\n"
    "Остальное — кнопками в меню."
)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db: Database) -> None:
    await state.clear()
    user = message.from_user
    await db.upsert_user(user.id, user.username, user.full_name)
    await message.answer(
        f"Привет, {hbold(user.full_name)}! 👋\n\n{HELP_TEXT}",
        reply_markup=main_menu,
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=main_menu)


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    if await state.get_state() is None:
        await message.answer("Нечего отменять.", reply_markup=main_menu)
        return
    await state.clear()
    await message.answer("Отменил. Возвращаю в меню.", reply_markup=main_menu)


@router.message(F.text == "👤 Профиль")
async def show_profile(message: Message, db: Database) -> None:
    user = message.from_user
    total = await db.count_requests(user.id)
    await message.answer(
        f"{hbold('Твой профиль')}\n"
        f"ID: <code>{user.id}</code>\n"
        f"Имя: {user.full_name}\n"
        f"Username: @{user.username or '—'}\n"
        f"Заявок отправлено: {total}"
    )


@router.message(F.text == "ℹ️ О боте")
async def about(message: Message) -> None:
    await message.answer(
        "Шаблон бота на aiogram 3: меню, FSM-сценарий заявки, SQLite и админ-команды.\n"
        "Дальше наполняй своей логикой."
    )


@router.message()
async def fallback(message: Message) -> None:
    await message.answer("Не понял. Нажми кнопку в меню или /help.", reply_markup=main_menu)
