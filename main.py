import logging
import os
import requests
import re
from dotenv import load_dotenv
from flask import Flask
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          ContextTypes, filters)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Flask server for uptime
app = Flask(__name__)


@app.route('/')
def home():
    return "✅ Bot is alive!"


# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# User tracking + Admin
users = set()
ADMIN_IDS = [6838940621]  # Replace with your Telegram ID


# /admin
async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 You are not authorized to use this."
                                        )
        return
    await update.message.reply_text(
        "🛠 *Admin Panel*\n"
        "• /users – Show total users\n"
        "• /broadcast <message> – Send message to all users",
        parse_mode="Markdown")


# /users
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Not authorized.")
        return
    await update.message.reply_text(f"👥 Total users: {len(users)}")


# /broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Not authorized.")
        return
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("⚠️ Usage: /broadcast <your message>")
        return
    count = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg)
            count += 1
        except:
            pass
    await update.message.reply_text(f"✅ Message sent to {count} users.")


# /start (no keyboard)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to SmartxHacker Bot!\nAsk me anything...",
        reply_markup=ReplyKeyboardRemove())


# /download
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 Download Smart Tunnel App:\nhttps://smarttunnel.in/smarttunnel.apk")


# /website
async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Visit official site:\nhttps://smarttunnel.in")


# /contact
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📬 Message SmartxHacker:\nhttps://t.me/smartxhacker")


# OpenRouter AI
def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/your_bot_username"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{
            "role": "user",
            "content": prompt
        }],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.text}"


# Text handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    users.add(update.effective_user.id)

    # Simple keyword triggers
    if "download app" in user_input:
        await update.message.reply_text(
            "📥 Download Smart Tunnel App:\nhttps://smarttunnel.in/smarttunnel.apk"
        )
        return
    if "official website" in user_input:
        await update.message.reply_text(
            "🌐 Visit official site:\nhttps://smarttunnel.in")
        return
    if "contact smartxhacker" in user_input:
        await update.message.reply_text(
            "📬 Message SmartxHacker:\nhttps://t.me/smartxhacker")
        return

    # Bot identity
    if any(kw in user_input
           for kw in ["smart tunnel", "smart tunnel app", "download tunnel"]):
        await update.message.reply_text(
            "📥 Download Smart Tunnel App:\nhttps://smarttunnel.in/smarttunnel.apk"
        )
        return

    if any(kw in user_input for kw in [
            "who is your master", "who is your creator", "who is your owner",
            "where is your master", "your master", "your creator", "your boss",
            "your owner", "who made you", "who created you"
    ]):
        await update.message.reply_text(
            "👑 My master is *Farhan Ansari*\n📬 [Click to Message](https://t.me/smartxhacker)",
            parse_mode="Markdown")
        return

    if "farhan" in user_input:
        await update.message.reply_text(
            "📬 Contact Farhan Ansari:\n[Click to Message](https://t.me/smartxhacker)",
            parse_mode="Markdown")
        return

    # "I am <name>" custom replies
    match = re.search(r"\b(i am|i'm)\s+(\w+)", user_input)
    if match:
        person_name = match.group(2).capitalize()
        custom_replies = {
            "Farhan":
            "Hello Sir, Welcome 😎",
            "Krishna":
            "Hello Krishna! Welcome to the bot.",
            "Falak":
            "Hello! Mrs. Ansari, how are you? Are you looking for my Master?"
        }
        await update.message.reply_text(
            custom_replies.get(person_name,
                               f"Hello {person_name}, nice to meet you!"))
        return

    # Fallback AI reply
    reply = ask_openrouter(user_input)
    await update.message.reply_text(reply)


# Flask runner
def run_server():
    app.run(host='0.0.0.0', port=8080)


# Launch bot
def main():
    import threading
    threading.Thread(target=run_server).start()

    logging.basicConfig(level=logging.INFO)
    bot = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("admin", admin_menu))
    bot.add_handler(CommandHandler("users", list_users))
    bot.add_handler(CommandHandler("broadcast", broadcast))
    bot.add_handler(CommandHandler("download", download))
    bot.add_handler(CommandHandler("website", website))
    bot.add_handler(CommandHandler("contact", contact))

    # Text message handler
    bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    bot.run_polling()


main()
