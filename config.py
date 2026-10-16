"""Настройки бота: читаются из переменных окружения (.env)."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _parse_admins(raw: str) -> list[int]:
    return [int(x) for x in raw.replace(" ", "").split(",") if x]


@dataclass(frozen=True)
class Config:
    bot_token: str
    admins: list[int] = field(default_factory=list)
    db_path: str = "bot.db"

    @classmethod
    def load(cls) -> "Config":
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise RuntimeError(
                "BOT_TOKEN не задан. Скопируй .env.example в .env и впиши токен от @BotFather."
            )
        return cls(
            bot_token=token,
            admins=_parse_admins(os.getenv("ADMINS", "")),
            db_path=os.getenv("DB_PATH", "bot.db"),
        )


config = Config.load()
