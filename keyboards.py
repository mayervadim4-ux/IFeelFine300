"""Клавиатуры бота."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="📝 Оставить заявку")],
        [KeyboardButton(text="ℹ️ О боте")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери пункт меню",
)


def confirm_kb(action: str) -> InlineKeyboardMarkup:
    """Инлайн-кнопки подтверждения. callback_data: confirm:<action> / cancel:<action>."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Отправить", callback_data=f"confirm:{action}"),
                InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel:{action}"),
            ]
        ]
    )
