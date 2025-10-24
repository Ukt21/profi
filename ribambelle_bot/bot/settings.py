from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
# Укажи свой ID менеджера (или чат-бота менеджеров)
MANAGERS_CHAT_ID = int(os.getenv("MANAGERS_CHAT_ID", "0"))
DB_PATH = os.getenv("DB_PATH", "./bot.db")
PROMO_VALID_DAYS = int(os.getenv("PROMO_VALID_DAYS", "30"))
SECRET_KEY = os.getenv("SECRET_KEY", "change_me")

# Опционально (если нужен экспорт в Google Sheets)
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
