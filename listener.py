import time
import requests
from config import TELEGRAM_BOT_TOKEN
from bot_commands import handle_command

API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def get_updates(offset=None):
    url = f"{API}/getUpdates?timeout=15"
    if offset:
        url += f"&offset={offset}"
    res = requests.get(url).json()
    return res.get("result", [])

if __name__ == "__main__":
    last_update = None

    while True:
        updates = get_updates(last_update)
        for u in updates:
            last_update = u["update_id"] + 1

            if "message" in u and "text" in u["message"]:
                text = u["message"]["text"]
                handle_command(text)

        time.sleep(1)
