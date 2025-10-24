from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from ..keyboards.inline import admin_menu
from ..db.models import get_stats, export_feedback_csv
from ..texts.ru import ADMIN_ONLY
import os

router = Router()

@router.message(F.text == "/admin")
async def admin_entry(message: Message, is_admin: bool):
    if not is_admin:
        return await message.answer(ADMIN_ONLY)
    await message.answer("Панель менеджера:", reply_markup=admin_menu())

@router.callback_query(F.data == "admin_stats")
async def admin_stats(call: CallbackQuery, is_admin: bool):
    if not is_admin:
        return await call.answer("Нет доступа", show_alert=True)
    stats = get_stats()
    await call.message.answer(f"📊 Отзывов: {stats['total']}\n⭐ Средняя: {stats['avg']}")
    await call.answer()

@router.callback_query(F.data == "admin_export")
async def admin_export(call: CallbackQuery, is_admin: bool):
    if not is_admin:
        return await call.answer("Нет доступа", show_alert=True)
    path = "feedback_export.csv"
    export_feedback_csv(path)
    await call.message.answer_document(document=open(path, "rb"), caption="Экспорт отзывов (CSV)")
    await call.answer()

@router.callback_query(F.data == "admin_promo")
async def admin_promo(call: CallbackQuery, is_admin: bool):
    if not is_admin:
        return await call.answer("Нет доступа", show_alert=True)
    await call.message.answer("Промокоды генерируются автоматически при оценке 4–5 ⭐.")
    await call.answer()
