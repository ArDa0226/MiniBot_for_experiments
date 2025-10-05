from cgitb import handler
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

from handlers.user import user_router

CACHE = TTLCache(maxsize=10_000, ttl=5)

class ThrottlingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handlers: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")

        if user.id in CACHE:
            return

        CACHE[user.id] = True

        return await handler(event, data)

