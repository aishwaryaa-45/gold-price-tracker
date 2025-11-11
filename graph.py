import sqlite3
import matplotlib.pyplot as plt

PRODUCT_NAME = "Gold_Belagavi_24K_10g"   # <--- your exact product_name

def get_price_history():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, price FROM product_prices
        WHERE product_name = ?
        ORDER BY date ASC
    """, (PRODUCT_NAME,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_graph():
    history = get_price_history()

    if not history:
        print("No data found for this product yet.")
        return

    dates = [row[0] for row in history]
    prices = [row[1] for row in history]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker="o", linewidth=2)
    plt.title(f"Price Trend: {PRODUCT_NAME}")
    plt.xlabel("Date")
    plt.ylabel("Price (₹ per 10g)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("gold_trend.png")
    plt.show()

if __name__ == "__main__":
    generate_graph()
