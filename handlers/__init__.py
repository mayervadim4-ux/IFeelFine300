"""Роутеры бота. Порядок важен: общий роутер подключается последним."""

from aiogram import Router

from . import admin, common, request


def get_router() -> Router:
    router = Router(name="root")
    router.include_router(admin.router)
    router.include_router(request.router)
    router.include_router(common.router)
    return router
