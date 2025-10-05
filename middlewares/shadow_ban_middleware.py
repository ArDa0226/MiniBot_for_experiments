from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

CACHE = {
    "banned": [254443334, 214454432, 112221212],
}

class ShadowBanMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:

        user: User = data.get("event_from_user")
        if user is not None:
            if user.id in CACHE.get("banned"):
                return

        return await handler(event, data)
