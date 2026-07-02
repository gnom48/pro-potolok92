import requests
import sqlite3
import consts
from datetime import date, timedelta

# ================== Отчеты ==================


def generate_report():
    '''Генерация отчёта'''
    conn = sqlite3.connect(consts.DB_FILE)
    cur = conn.cursor()
    report_date = (date.today() - timedelta(days=1)).isoformat()

    cur.execute("""
        SELECT count
        FROM daily_visits
        WHERE visit_date = ?
    """, (report_date,))
    total_visits = cur.fetchone()
    total_visits = total_visits[0] if total_visits else 0

    conn.close()

    report = (
        f"Отчёт за {report_date} (PRO Потолок):\n\n"
        f"Посещений сайта: {total_visits}\n"
        f"Статистика агрегированная, без IP, User-Agent и персональных данных.\n"
    )
    return report


def send_report():
    '''Отправка отчёта'''
    report = generate_report()
    for chat_id in consts.CHAT_IDS:
        requests.post(
            f"https://api.telegram.org/bot{consts.TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": report}
        )
