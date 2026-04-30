# ChainCast Bot

ChainCast is a Telegram bot that delivers **AI-powered crypto and forex market insights** in a clean, easy-to-read format.

It pulls real-time news from trusted sources and uses AI to summarize, analyze, and extract actionable signals for traders and investors.

---

## Features

* 📰 **Crypto News Summary**
  Get the latest crypto headlines summarized with key insights.

* 💱 **Forex News Summary**
  Stay updated with major forex market events and macro trends.

* 📈 **Bullish Signals**
  Extract potential upside opportunities from current news.

* 📉 **Bearish Signals**
  Identify downside risks and negative market sentiment.

* 🪙 **Bitcoin Analysis (BTC)**
  Quick outlook based on recent developments.

* 🥇 **Gold Analysis (XAUUSD)**
  Macro-driven analysis for gold traders.

---

## Commands

```
/cryptonews  → AI summary of crypto news  
/forexnews   → AI summary of forex news  

/bullish     → Extract bullish opportunities  
/bearish     → Extract bearish signals  

/btc         → Bitcoin trend & outlook  
/gold        → Gold (XAUUSD) analysis  

/help        → Show command guide
```

---

## How It Works

1. Fetches latest news via RSS feeds
2. Sends raw data to AI (JUNE API)
3. AI analyzes and structures insights
4. Output is cleaned and formatted for Telegram

---

## Tech Stack

* Python
* python-telegram-bot
* Feedparser (RSS parsing)
* Requests (API calls)
* JUNE AI API

---

## Environment Variables

Create a `.env` file:

```
TELEGRAM_TOKEN=your_telegram_bot_token
JUNE_API_KEY=your_june_api_key
```

---

## ▶️ Run Locally

```
pip install -r requirements.txt
python bot.py
```

---

## Notes

* Telegram message limit is handled (max 4000 chars)
* Output is auto-cleaned for readability
* Built for educational & trading insight purposes

---

## Author

Built by Markje
Exploring AI, trading, and Web3 🚀
