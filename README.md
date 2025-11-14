# Gold Price Trend Monitor & Telegram Alert Bot

This project automatically tracks **24K retail gold prices per 10g** for a selected city, stores historical data, analyzes trends, generates insight, and sends **daily updates to Telegram**.

## ✅ Features
- Fetches **real retail gold rate per 10g**
- Stores historical prices in **SQLite**
- Generates **daily trend graphs**
- Uses **Groq LLaMA 3.1-8B model** to provide market insight
- Sends **Telegram alerts** automatically
- Runs hands-free using **Task Scheduler / cron**

## 🧠 Why This Project Exists
Gold rates change daily and fluctuate based on:
- Import duties
- INR-USD currency movement
- Local retail markup
- Seasonal demand spikes

This bot tracks price movement objectively — without guesswork — and notifies when the market is in a **watch**, **wait**, or **buy** zone.

## 🏗 Tech Stack
| Component | Technology |
|----------|------------|
| Scraping | `requests`, `BeautifulSoup4` |
| Data Storage | SQLite (`prices.db`) |
| Visualization | `matplotlib` |
| AI Analysis | Groq LLaMA 3.1 models (`groq` Python client) |
| Alerts | Telegram Bot API |
| Automation | Windows Task Scheduler  |

## 📂 Project Structure
price-tracker/
│
├── fetch_prices.py # Retrieves gold price (per 10g)
├── db.py # Database init + insert logic
├── track_all.py # Daily tracking entry point
├── send_graph.py # Creates graph + sends Telegram message
├── analysis_ai.py # Trend reasoning using LLaMA model
├── trend_math.py # Pure math-based price signal logic
│
├── config.py # API keys + bot tokens
└── prices.db # Historical logged data

## 🚀 Running the Bot
1. Activate virtual environment
2. Run tracking manually:
3. Run daily Telegram send:
To automate:
- Use **Windows Task Scheduler** → run both scripts daily.
## 📌 Status
✅ Fully functional  
✅ Zero manual interaction  
✅ Safe from API billing issues
