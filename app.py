from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import consts
import os
from scheduler import send_report


class MyFlask(Flask):
    def __init__(
        self,
        import_name: str,
        static_url_path: str | None = None,
        static_folder: str | os.PathLike[str] | None = "static",
        static_host: str | None = None,
        host_matching: bool = False,
        subdomain_matching: bool = False,
        template_folder: str | os.PathLike[str] | None = "templates",
        instance_path: str | None = None,
        instance_relative_config: bool = False,
        root_path: str | None = None,
    ):
        self.my_scheduler = BackgroundScheduler(timezone="UTC")
        self.my_scheduler.add_job(
            send_report, trigger=CronTrigger(hour=9+3, minute=0))
        self.my_scheduler.start()

        super().__init__(
            import_name=import_name,
            static_url_path=static_url_path,
            static_folder=static_folder,
            static_host=static_host,
            host_matching=host_matching,
            subdomain_matching=subdomain_matching,
            template_folder=template_folder,
            instance_path=instance_path,
            instance_relative_config=instance_relative_config,
            root_path=root_path,
        )


def create_app() -> Flask:
    return MyFlask(__name__, static_folder="static", template_folder="templates")


app = create_app()

# ================== База данных ==================


def init_db():
    conn = sqlite3.connect(consts.DB_FILE)
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
        conn = sqlite3.connect(consts.DB_FILE)
        cur = conn.cursor()
        cur.execute("INSERT INTO visits (ip, user_agent, timestamp) VALUES (?, ?, ?)",
                    (ip, user_agent, now))
        conn.commit()
        conn.close()


# ================== Основные маршруты ==================


@app.route('/api/reviews')
def get_reviews():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(consts.YANDEX_URL, headers=headers)
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


init_db()
