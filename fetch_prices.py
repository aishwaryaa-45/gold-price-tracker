import requests
from bs4 import BeautifulSoup
import re

def fetch_gold_price():
    url = "https://www.goldrate.com/en/gold/india/belgaum"
    print("Scraping:", url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    # Extract 24k gold per gram from the sentence:
    # "The price of Gold in India today is ₹12,227.87 per gram for 24k gold ..."
    match = re.search(r"24k gold[^₹]*₹([\d,]+\.\d+)", text, re.IGNORECASE)

    if not match:
        raise Exception("24K gold price not found")

    per_gram = float(match.group(1).replace(",", ""))
    per_10g = per_gram * 10

    print("24K per gram:", per_gram)
    print("24K per 10g:", per_10g)

    return per_10g
