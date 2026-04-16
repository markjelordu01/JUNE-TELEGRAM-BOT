from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser
import requests

# 🔑 KEYS
TELEGRAM_TOKEN = "8787117098:AAF8hrlfNcxkPkY-siheN5q6TUVMK3sRAg0"
JUNE_API_KEY = "sk_live_e23842c4cd1d415eb5f205402fc519e00bf8e9b272814e63baa83e71879808e2"

# 📰 GET CRYPTO NEWS
def get_crypto_news():
    feed = feedparser.parse("https://cointelegraph.com/rss")
    entries = feed.entries[:3]

    news = ""
    for entry in entries:
        news += f"{entry.title}\n{entry.summary}\n\n"

    return news

# 🤖 SUMMARIZE USING AI
def summarize(news_text):
    prompt = f"""
Summarize these crypto news into CLEAN Telegram format.

Rules:
- Use emojis
- Add proper spacing
- Make it readable
- Separate each news with a line

Format EXACTLY like this:

📰 Crypto News Update

1️⃣ [Title]

📌 Key Points:
• point 1
• point 2
• point 3

📊 Sentiment: [Bullish/Bearish/Neutral]

💡 Why it matters:
[short explanation]

━━━━━━━━━━━━━━

Repeat for each news.

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
                {"role": "system", "content": "You are a professional crypto news analyst."},
                {"role": "user", "content": prompt}
            ]
        }
    )

    print("DEBUG:", response.text)

    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "⚠️Error Response"

# 📲 COMMAND
async def cryptonews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Fetching latest crypto news...\n")

    news = get_crypto_news()
    summary = summarize(news)

    # ✨ CLEAN OUTPUT
    summary = summary.replace("**", "")

    await update.message.reply_text(summary)

# 🚀 START BOT
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("cryptonews", cryptonews))

print("Bot is running... 🚀")
app.run_polling()