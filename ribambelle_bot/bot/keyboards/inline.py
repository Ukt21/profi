from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🗂 Экспорт CSV", callback_data="admin_export")],
        [InlineKeyboardButton(text="🎁 Сгенерировать промокод", callback_data="admin_promo")],
    ])
