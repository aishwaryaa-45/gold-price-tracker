# analysis_ai.py (Groq version)

import sqlite3
from groq import Groq

from config import GROQ_API_KEY

DB_PATH = "prices.db"

client = Groq(api_key=GROQ_API_KEY)

def get_history(product_name, limit=7):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, price FROM product_prices
        WHERE product_name = ?
        ORDER BY date ASC
    """, (product_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows[-limit:]

def explain_trend(product_name="Gold_Belagavi_24K_10g"):
    history = get_history(product_name)

    if len(history) < 3:
        return "Not enough data for market interpretation yet."

    prices = [p for (_, p) in history]
    latest = prices[-1]
    prev = prices[-2]

    prompt = f"""
    Recent gold prices: {prices}
    Latest price: {latest}
    Previous price: {prev}

    Give a short actionable analysis:
    - Is the price trending up or down?
    - Should the user buy now or wait?
    Make the answer crisp and practical.
    """

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
