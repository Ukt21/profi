from aiogram import Router
from aiogram.types import Update
import logging

router = Router()
log = logging.getLogger(__name__)

@router.errors()
async def errors_handler(update: Update, exception: Exception):
    log.exception("Unhandled exception: %s", exception)
    return True
