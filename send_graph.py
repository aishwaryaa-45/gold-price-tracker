import sqlite3
import requests
import io
import matplotlib
matplotlib.use("Agg")  # Run without GUI
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from trend_math import analyze_trend

PRODUCT_NAME = "Gold_Belagavi_24K_10g"
DB_PATH = "prices.db"


def get_history(product_name, days=7):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, price FROM product_prices
        WHERE product_name = ?
        ORDER BY date ASC
    """, (product_name,))
    rows = cursor.fetchall()
    conn.close()

    # Keep latest entry per day
    merged = {}
    for d, p in rows:
        merged[d] = p

    dates = sorted(merged.keys())
    prices = [merged[d] for d in dates]

    # Return last N days
    return dates[-days:], prices[-days:]


def send_text(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})


def send_graph(dates, prices):
    xs = [datetime.fromisoformat(d) for d in dates]

    plt.figure(figsize=(8, 4.5))
    plt.plot(xs, prices, marker="o", linewidth=2)

    plt.title(f"{PRODUCT_NAME} Trend (per 10g)")
    plt.xlabel("Date")
    plt.ylabel("Price (₹)")

    # ✅ Clean date formatting
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # e.g., Nov 08
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=30)

    plt.grid(True, linestyle="--", alpha=0.35)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    requests.post(url, files={"photo": buf}, data={"chat_id": TELEGRAM_CHAT_ID})


if __name__ == "__main__":
    print("↻ Fetching history...")
    dates, prices = get_history(PRODUCT_NAME, days=7)

    print("Dates:", dates)
    print("Prices:", prices)

    if len(prices) < 2:
        send_text(f"Not enough data yet to generate graph.\nLatest Price: ₹{prices[-1] if prices else 'N/A'}")
        print("⚠️ Not enough data. Sent text instead.")
    else:
        send_graph(dates, prices)
        send_text(f"📊 Gold Trend Updated! Latest: ₹{prices[-1]}")
        print("✅ Graph sent successfully.")
        
        recommendation = analyze_trend(PRODUCT_NAME)
        send_text("💡 Recommendation:\n" + recommendation)
        
        from analysis_ai import explain_trend
        insight = explain_trend(PRODUCT_NAME)
        send_text("🧠 Insight:\n" + insight)

        

