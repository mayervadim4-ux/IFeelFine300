"""Сценарий «оставить заявку» на FSM: текст → подтверждение → сохранение."""

import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from config import config
from db import Database
from keyboards import confirm_kb, main_menu

logger = logging.getLogger(__name__)
router = Router(name="request")

MAX_LEN = 1000


class RequestForm(StatesGroup):
    text = State()
    confirm = State()


@router.message(F.text == "📝 Оставить заявку")
async def start_request(message: Message, state: FSMContext) -> None:
    await state.set_state(RequestForm.text)
    await message.answer(
        "Опиши заявку одним сообщением. /cancel — отмена.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(RequestForm.text, F.text)
async def got_text(message: Message, state: FSMContext) -> None:
    text = message.text.strip()
    if len(text) > MAX_LEN:
        await message.answer(f"Слишком длинно ({len(text)}), уложись в {MAX_LEN} символов.")
        return

    await state.update_data(text=text)
    await state.set_state(RequestForm.confirm)
    await message.answer(
        f"Проверь заявку:\n\n<i>{text}</i>",
        reply_markup=confirm_kb("request"),
    )


@router.message(RequestForm.text)
async def wrong_type(message: Message) -> None:
    await message.answer("Жду текст. Либо /cancel.")


@router.callback_query(RequestForm.confirm, F.data == "confirm:request")
async def save_request(call: CallbackQuery, state: FSMContext, db: Database, bot: Bot) -> None:
    data = await state.get_data()
    text = data.get("text", "")
    request_id = await db.add_request(call.from_user.id, text)
    await state.clear()

    await call.message.edit_text(f"✅ Заявка #{request_id} принята.")
    await call.answer()
    await call.message.answer("Чем ещё помочь?", reply_markup=main_menu)

    for admin_id in config.admins:
        try:
            await bot.send_message(
                admin_id,
                f"🆕 Заявка #{request_id} от {call.from_user.full_name} "
                f"(<code>{call.from_user.id}</code>):\n\n{text}",
            )
        except Exception:  # админ мог не запускать бота или заблокировать его
            logger.warning("Не удалось уведомить админа %s", admin_id, exc_info=True)


@router.callback_query(RequestForm.confirm, F.data == "cancel:request")
async def cancel_request(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("❌ Заявка отменена.")
    await call.answer()
    await call.message.answer("Возвращаю в меню.", reply_markup=main_menu)
