from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser
import requests
import os

# KEYS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
JUNE_API_KEY = os.getenv("JUNE_API_KEY")


# GET CRYPTO NEWS
def get_crypto_news():
    feed = feedparser.parse("https://cointelegraph.com/rss")
    entries = feed.entries[:3]

    news = ""
    for entry in entries:
        news += f"{entry.title}\n{entry.summary}\n\n"

    return news

# GET FOREX NEWS
def get_forex_news():
    feed = feedparser.parse("https://www.forexlive.com/feed/")
    entries = feed.entries[:3]

    if not entries:
        return "No forex news available right now."
    
    news = ""
    for entry in entries:
        news += f"{entry.title}\n{entry.summary}\n\n"

    return news

async def forexnews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💱 Fetching latest forex news...\n")

    news = get_forex_news()
    summary = summarize(news, mode="forex")

    summary = summary.replace("**", "")

    await update.message.reply_text(summary)

#SUMMARIZE
def summarize(news_text, mode="crypto"):
    
    if mode == "crypto":
        intro = "You are a crypto market analyst."
    else:
        intro = "You are a forex market analyst."

    prompt = f"""
Summarize these {mode} news.

Format:
Title
Key Points (3 bullets)
Sentiment (Bullish/Bearish/Neutral)
Why it matters

News:
{news_text}
"""

    response = requests.post(
        "https://api.blockchain.info/ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {JUNE_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "blockchain/june",
            "messages": [
                {"role": "system", "content": intro},
                {"role": "user", "content": prompt}
            ]
        }
    )

    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "⚠️ Error sa AI response"

#COMMAND
async def cryptonews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Fetching latest crypto news...\n")

    news = get_crypto_news()
    summary = summarize(news)

    #CLEAN OUTPUT
    summary = summary.replace("**", "")

    await update.message.reply_text(summary)

#TART BOT
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("cryptonews", cryptonews))
app.add_handler(CommandHandler("forexnews", forexnews))

print("Bot is running... 🚀")
app.run_polling()