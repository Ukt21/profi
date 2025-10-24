from aiogram import Bot

async def notify_manager(bot: Bot, chat_id: int, text: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception:
        pass
