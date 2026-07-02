import sqlite3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

import consts


def generate_report():
    report_date = (datetime.now(ZoneInfo(consts.TIMEZONE)).date() - timedelta(days=1)).isoformat()

    conn = sqlite3.connect(consts.DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT count
        FROM daily_visits
        WHERE visit_date = ?
    """, (report_date,))
    row = cur.fetchone()
    conn.close()

    visitors = row[0] if row else 0
    return (
        f"Отчет PRO Потолок за {report_date}:\n"
        f"Посетителей сайта: {visitors}\n"
        f"Данные обезличены: хранится только дата и число посетителей."
    )


def send_report():
    if not consts.TELEGRAM_TOKEN or not consts.CHAT_IDS:
        return

    report = generate_report()
    for chat_id in consts.CHAT_IDS:
        requests.post(
            f"https://api.telegram.org/bot{consts.TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": report},
            timeout=10
        )
