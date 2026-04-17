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
    summary = clean_format(summary)
    await update.message.reply_text(summary[:4000])

#SUMMARIZE
def summarize(text, mode="crypto"):

    if mode == "crypto":
        intro = "You are a crypto market analyst."
    else:
        intro = "You are a forex market analyst."

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
                {"role": "user", "content": text}
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
    summary = clean_format(summary)
    await update.message.reply_text(summary[:4000])

#Bullish
async def bullish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Finding bullish signals...\n")

    news = get_crypto_news()
    
    prompt = f"""
From this news, extract only BULLISH signals.

Format:
- Asset:
- Reason:
- Confidence (Low/Medium/High)

News:
{news}
"""
    result = summarize(prompt, mode="crypto")
    result = result.replace("**", "")
    summary = clean_format(summary)
    await update.message.reply_text(result[:4000])

#Bearish
async def bearish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📉 Finding bearish signals...\n")

    news = get_crypto_news()
    
    prompt = f"""
From this news, extract only BEARISH signals.

Format:
- Asset:
- Reason:
- Confidence (Low/Medium/High)
News:
{news}
"""
    result = summarize(prompt, mode="crypto")
    result = result.replace("**", "")
    summary = clean_format(summary)
    await update.message.reply_text(result[:4000])

#BTC
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪙 Analyzing Bitcoin...\n")

    news = get_crypto_news()

    prompt = f"""
Analyze Bitcoin (BTC) based on this news.

Format:
- Trend: (Bullish/Bearish/Neutral)
- Key Drivers:
- Short-term Outlook:

News:
{news}
"""
    result = summarize(prompt, mode="crypto")
    result = result.replace("**", "")
    summary = clean_format(summary)
    await update.message.reply_text(result[:4000])

#GOLD
async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🥇 Analyzing Gold (XAUUSD)...\n")

    news = get_forex_news()

    prompt = f"""
Analyze Gold (XAUUSD) based on this news.

Format:
- Trend: (Bullish/Bearish/Neutral)
- Key Drivers:
- Outlook:

News:
{news}
"""
    result = summarize(prompt, mode="forex")
    result = result.replace("**", "")
    summary = clean_format(summary)
    await update.message.reply_text(result[:4000])

#START MESSAGE
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
🤖 Welcome to ChainCast Bot!

Available Commands:

📰 /cryptonews - Latest crypto news  
💱 /forexnews - Latest forex news  

📈 /bullish - Bullish signals  
📉 /bearish - Bearish signals  

🪙 /btc - Bitcoin analysis  
🥇 /gold - Gold (XAUUSD) analysis  

ℹ️ /help - Show commands again
"""

    await update.message.reply_text(message)

#HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
📖 Command Guide:

/cryptonews → AI summary of crypto news  
/forexnews → AI summary of forex news  

/bullish → Extract bullish opportunities  
/bearish → Extract bearish signals  

/btc → Bitcoin trend & outlook  
/gold → Gold (XAUUSD) analysis  

🚀 Powered by AI
"""

    await update.message.reply_text(message)

def clean_format(text):
    # remove HTML breaks
    text = text.replace("<br>", "\n")

    # remove pipes (|)
    text = text.replace("|", "")

    # fix spacing
    text = text.replace("\n\n\n", "\n\n")

    # optional: add spacing before sections
    text = text.replace("Key Points:", "\n📌 Key Points:")
    text = text.replace("Sentiment:", "\n📊 Sentiment:")
    text = text.replace("Why it matters:", "\n💡 Why it matters:")
    text = text.replace("Trend:", "\n📈 Trend:")
    text = text.replace("Outlook:", "\n🔮 Outlook:")

    return text.strip()


#TART BOT
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("cryptonews", cryptonews))
app.add_handler(CommandHandler("forexnews", forexnews))
app.add_handler(CommandHandler("bullish", bullish))
app.add_handler(CommandHandler("bearish", bearish))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("gold", gold))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

print("Bot is running... 🚀")
app.run_polling()