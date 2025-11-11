import sqlite3
import statistics

DB_PATH = "prices.db"

def get_prices(product_name, limit=7):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT price FROM product_prices
        WHERE product_name = ?
        ORDER BY date DESC
        LIMIT ?
    """, (product_name, limit))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows][::-1]  # return oldest→newest order

def analyze_trend(product_name="Gold_Belagavi_24K_10g"):
    prices = get_prices(product_name, 7)
    
    if len(prices) < 3:
        return "Not enough data for trend recommendation yet."

    last = prices[-1]
    prev = prices[-2]
    ma7 = statistics.mean(prices)

    # Momentum (direction strength)
    momentum = last - prev

    if last < ma7 and momentum < 0:
        return f"BUY — price is dipping below 7-day average.\nCurrent: ₹{last:,.0f}, Avg: ₹{ma7:,.0f}"
    elif last > ma7 and momentum > 0:
        return f"WAIT — price is rising above trend.\nCurrent: ₹{last:,.0f}, Avg: ₹{ma7:,.0f}"
    else:
        return f"WATCH — no strong trend yet.\nCurrent: ₹{last:,.0f}, Avg: ₹{ma7:,.0f}"
