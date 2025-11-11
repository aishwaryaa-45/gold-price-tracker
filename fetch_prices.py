import requests
import re
from config import SERPAPI_KEY

def extract_price(text):
    # Find prices like 5,865 or 5865 or 5865.50 or ₹5865
    matches = re.findall(r"₹?\s?(\d[\d,]*\.?\d*)", text)
    if not matches:
        return None

    # Convert all found matches to floats
    numbers = [float(m.replace(",", "")) for m in matches]

    # Filter out small numbers (like 24 from "24K")
    numbers = [n for n in numbers if n > 100]  # gold price per gram is always > ₹100

    return numbers[0] if numbers else None


def fetch_gold_price(city="Belagavi"):
    query = f"24K gold price today {city}"

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    data = requests.get(url, params=params).json()

    # 1) Try structured answer box → e.g. "₹5,865"
    answer_box = data.get("answer_box", {})
    if "prices" in answer_box and "value" in answer_box["prices"]:
        price_text = answer_box["prices"]["value"]
        price = extract_price(price_text)
        if price:
            return price

    # 2) Try answer_box "snippet" or description
    for key in ["snippet", "answer", "title"]:
        if key in answer_box:
            price = extract_price(str(answer_box[key]))
            if price:
                return price

    # 3) Try organic search results
    organic_results = data.get("organic_results", [])
    for result in organic_results:
        snippet = result.get("snippet", "")
        price = extract_price(snippet)
        if price:
            return price

    # 4) Try shopping results (rare case)
    shopping = data.get("shopping_results", [])
    for item in shopping:
        price = extract_price(item.get("price", ""))
        if price:
            if price < 50000.00:
                price = price * 10
            return price

    # If we reach here → nothing matched
    raise Exception("❌ Could not extract gold price. Structure changed or no data returned.")
