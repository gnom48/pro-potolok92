import requests
import sqlite3
import consts

# ================== Отчеты ==================


def generate_report():
    '''Генерация отчёта'''
    conn = sqlite3.connect(consts.DB_FILE)
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


def send_report():
    '''Отправка отчёта'''
    report = generate_report()
    for chat_id in consts.CHAT_IDS:
        requests.post(
            f"https://api.telegram.org/bot{consts.TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": report}
        )
