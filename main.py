from flask import Flask, send_from_directory, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
from pytz import timezone

app = Flask(__name__)

# ================== Настройки ==================
YANDEX_URL = "https://yandex.ru/maps/org/214850144202/reviews"

TELEGRAM_TOKEN = "8348692489:AAEI3a8VJaNlMI4YDPAFE0kWNmmn7YUN5mM"
CHAT_IDS = ["1115007593", "5921894758"]  # список получателей

DB_FILE = "visitors.db"


# ================== База данных ==================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user_agent TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ================== Логирование визитов ==================
@app.before_request
def log_visit():
    if request.endpoint not in ("static", "get_reviews"):  # не считаем API и статику
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent", "Unknown")

        # фильтрация ботов
        bot_signatures = ["bot", "spider", "crawl"]
        if any(b in user_agent.lower() for b in bot_signatures):
            return

        now = datetime.now()
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO visits (ip, user_agent, timestamp) VALUES (?, ?, ?)",
                    (ip, user_agent, now))
        conn.commit()
        conn.close()


# ================== Генерация отчёта ==================
def generate_report():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(DISTINCT ip) 
        FROM visits
        WHERE timestamp >= datetime('now', '-1 day')
    """)
    unique_visitors = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) 
        FROM visits
        WHERE timestamp >= datetime('now', '-1 day')
    """)
    total_visits = cur.fetchone()[0]

    conn.close()

    report = (
        f"📊 Отчёт за последние 24 часа (PRO Потолок):\n\n"
        f"👥 Уникальных посетителей: {unique_visitors}\n"
        f"🔄 Всего визитов: {total_visits}\n"
    )
    return report


# ================== Отправка отчёта ==================
def send_report():
    report = generate_report()
    for chat_id in CHAT_IDS:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": report}
        )


# ================== Основные маршруты ==================
@app.route('/api/reviews')
def get_reviews():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(YANDEX_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    reviews = []
    for review_block in soup.select(".review__body"):
        author = review_block.select_one(".review__author-name")
        text = review_block.select_one(".review__text")
        rating = review_block.select_one(".rating")
        reviews.append({
            "author": author.text.strip() if author else "Аноним",
            "text": text.text.strip() if text else "",
            "rating": rating.text.strip() if rating else "—"
        })

    return jsonify({"reviews": reviews})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        scheduler = BackgroundScheduler(timezone=timezone("Europe/Moscow"))
        scheduler.add_job(send_report, "cron", hour=12, minute=3)  
        scheduler.start()

    app.run(debug=True)
