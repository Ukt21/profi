import time
from aiogram import BaseMiddleware

class Throttling(BaseMiddleware):
    def __init__(self, rate: float = 0.5):
        self.rate = rate
        self.users = {}

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if not user:
            return await handler(event, data)
        now = time.time()
        last = self.users.get(user.id, 0.0)
        if now - last < self.rate:
            return  # гасим флуд
        self.users[user.id] = now
        return await handler(event, data)
