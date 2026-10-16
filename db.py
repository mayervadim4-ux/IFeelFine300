"""Простое хранилище на SQLite (aiosqlite)."""

import aiosqlite

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id    INTEGER PRIMARY KEY,
    username   TEXT,
    full_name  TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS requests (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    text       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


class Database:
    def __init__(self, path: str) -> None:
        self._path = path

    async def init(self) -> None:
        async with aiosqlite.connect(self._path) as conn:
            await conn.executescript(_SCHEMA)
            await conn.commit()

    async def upsert_user(self, user_id: int, username: str | None, full_name: str) -> None:
        async with aiosqlite.connect(self._path) as conn:
            await conn.execute(
                """
                INSERT INTO users (user_id, username, full_name) VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET username = excluded.username,
                                                   full_name = excluded.full_name
                """,
                (user_id, username, full_name),
            )
            await conn.commit()

    async def add_request(self, user_id: int, text: str) -> int:
        async with aiosqlite.connect(self._path) as conn:
            cursor = await conn.execute(
                "INSERT INTO requests (user_id, text) VALUES (?, ?)", (user_id, text)
            )
            await conn.commit()
            return cursor.lastrowid

    async def count_requests(self, user_id: int) -> int:
        async with aiosqlite.connect(self._path) as conn:
            async with conn.execute(
                "SELECT COUNT(*) FROM requests WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def stats(self) -> tuple[int, int]:
        """(всего пользователей, всего заявок)"""
        async with aiosqlite.connect(self._path) as conn:
            async with conn.execute("SELECT COUNT(*) FROM users") as cursor:
                users = (await cursor.fetchone())[0]
            async with conn.execute("SELECT COUNT(*) FROM requests") as cursor:
                requests = (await cursor.fetchone())[0]
        return users, requests
