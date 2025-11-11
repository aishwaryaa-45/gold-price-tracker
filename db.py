import sqlite3

def init_db():
    conn = sqlite3.connect("prices.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS product_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            store TEXT,
            price REAL,
            date TEXT
        )
    """)
    conn.close()

def save_price(product_name, store, price, date):
    conn = sqlite3.connect("prices.db")
    conn.execute("INSERT INTO product_prices (product_name, store, price, date) VALUES (?, ?, ?, ?)",
                 (product_name, store, price, date))
    conn.commit()
    conn.close()
