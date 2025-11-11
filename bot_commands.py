import sqlite3
import statistics
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from trend_math import analyze_trend
from analysis_ai import explain_trend

PRODUCT_NAME = "Gold_Belagavi_24K_10g"
DB_PATH = "prices.db"
API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def latest_price():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT date, price FROM product_prices
        WHERE product_name = ?
        ORDER BY date DESC LIMIT 1
    """, (PRODUCT_NAME,))
    row = cur.fetchone()
    conn.close()
    return row


def avg7():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT price FROM product_prices
        WHERE product_name = ?
        ORDER BY date DESC LIMIT 7
    """, (PRODUCT_NAME,))
    prices = [x[0] for x in cur.fetchall()]
    conn.close()

    if len(prices) < 2:
        return "Not enough data yet."
    return statistics.mean(prices)


def send(msg):
    requests.post(f"{API}/sendMessage", data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})


def handle_command(text):
    text = text.strip().lower()

    if text == "/today":
        d, p = latest_price()
        send(f"Today's Price (24K/10g): ₹{p:,.0f} ({d})")

    elif text == "/avg7":
        a = avg7()
        send(f"7-Day Average Price: ₹{a:,.0f}")

    elif text == "/trend":
        send(analyze_trend(PRODUCT_NAME))

    elif text == "/buy":
        send("Decision:\n" + analyze_trend(PRODUCT_NAME))

    elif text == "/insight":
        send("Market Interpretation:\n" + explain_trend(PRODUCT_NAME))

    else:
        send("Commands:\n/today\n/avg7\n/trend\n/buy\n/insight")
