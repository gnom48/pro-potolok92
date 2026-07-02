import os

YANDEX_URL = "https://yandex.ru/maps/org/214850144202/reviews"
DB_FILE = "visitors.db"
TIMEZONE = "Europe/Simferopol"

TELEGRAM_TOKEN = os.getenv("TOKEN", "")
CHAT_IDS = [chat_id.strip() for chat_id in os.getenv("CHAT_IDS", "").split(",") if chat_id.strip()]
