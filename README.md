# Telegram-бот (aiogram 3)

Рабочий шаблон: меню на кнопках, FSM-сценарий «заявка», SQLite, админ-команды.

## Структура

```
main.py          запуск бота (polling)
config.py        настройки из .env
db.py            SQLite: пользователи и заявки
keyboards.py     reply- и inline-клавиатуры
filters.py       фильтр IsAdmin
handlers/
  __init__.py    сборка роутеров
  common.py      /start, /help, /cancel, профиль, фолбэк
  request.py     сценарий заявки на FSM
  admin.py       /stats, /ping (только для ADMINS)
```

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

В `.env` впиши `BOT_TOKEN` от [@BotFather](https://t.me/BotFather) и свой ID в `ADMINS`
(узнать — [@userinfobot](https://t.me/userinfobot)).

## Как добавить свою команду

В `handlers/common.py`:

```python
@router.message(Command("myinfo"))
async def my_info(message: Message, db: Database) -> None:
    await message.answer("Привет!")
```

Новый раздел удобнее вынести отдельным файлом в `handlers/` со своим `router = Router()`
и подключить его в `handlers/__init__.py`. Фолбэк-хендлер в `common.py` ловит всё
подряд, поэтому его роутер подключается последним — новые роутеры добавляй выше него.

## Заметки

- `MemoryStorage` теряет состояния FSM при перезапуске. Для продакшена — `RedisStorage`.
- Каждый запрос к БД открывает своё соединение: просто и достаточно для небольшой
  нагрузки. На больших объёмах переходи на пул или SQLAlchemy.
