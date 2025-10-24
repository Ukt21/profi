from aiogram import BaseMiddleware
from ..settings import MANAGERS_CHAT_ID

class AdminACL(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data["is_admin"] = False
        user = getattr(event, "from_user", None)
        if user and user.id == MANAGERS_CHAT_ID:
            data["is_admin"] = True
        return await handler(event, data)
