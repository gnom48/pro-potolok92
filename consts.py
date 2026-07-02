import os
from dotenv import load_dotenv

load_dotenv()

YANDEX_URL = "https://yandex.ru/maps/org/214850144202/reviews"

TELEGRAM_TOKEN = os.getenv("TOKEN", default="NO TOKEN")
CHAT_IDS = ["1662173315"]

DB_FILE = "visitors.db"
