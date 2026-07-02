from flask import Flask, Response, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
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
        self.my_scheduler = BackgroundScheduler(timezone=consts.TIMEZONE)
        self.my_scheduler.add_job(send_report, trigger=CronTrigger(hour=9, minute=0))
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
SITE_URL = "https://pro-potolok92.ru"


# ================== Обезличенная статистика ==================


def init_db():
    conn = sqlite3.connect(consts.DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_visits (
            visit_date TEXT PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


@app.post('/api/visit')
def count_visit():
    today = datetime.now(ZoneInfo(consts.TIMEZONE)).date().isoformat()
    conn = sqlite3.connect(consts.DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO daily_visits (visit_date, count)
        VALUES (?, 1)
        ON CONFLICT(visit_date) DO UPDATE SET count = count + 1
    """, (today,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

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


@app.route('/robots.txt')
def robots_txt():
    sitemap_url = SITE_URL + "/sitemap.xml"
    content = f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n"
    return Response(content, mimetype="text/plain")


@app.route('/sitemap.xml')
def sitemap_xml():
    today = datetime.now(ZoneInfo(consts.TIMEZONE)).date().isoformat()
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{SITE_URL}/privacy</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
"""
    return Response(content, mimetype="application/xml")


init_db()
