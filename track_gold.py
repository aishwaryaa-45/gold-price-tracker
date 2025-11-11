from datetime import date
from sheet_reader import get_products
from fetch_prices import fetch_gold_price
from db import init_db, save_price

init_db()

products = get_products()

if not products:
    print("⚠️ No products found in sheet. Nothing to track.")
    exit()

for item in products:
    product_name = item["product_name"]
    city = product_name.split("_")[1] if "_" in product_name else product_name.replace("Gold_", "")

    try:
        price = fetch_gold_price(city)
        save_price(product_name, "Retail", price, str(date.today()))
        print(f"✅ Saved: {product_name} = {price}")
    except Exception as e:
        print(f"❌ Error while tracking {product_name}: {e}")
from analysis_ai import explain_trend
from alert import send_alert

summary = explain_trend("Gold_Belagavi_24K_10g")
send_alert("📊 Daily Gold Trend Update:\n\n" + summary)
print("📨 Sent Gemini daily analysis to Telegram")
