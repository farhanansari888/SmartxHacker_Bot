import logging
import os
import requests
import random
import re
import asyncio
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# === Environment Variables ===
TELEGRAM_BOT_TOKEN = os.environ.get("8036257083:AAFsJfmP-S0PwPraATrV-br1F-nKaNXbBJg")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# === Flask App ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive!"

# === Admin & User Tracking ===
users = set()
ADMIN_IDS = [6838940621]
GIRLFRIEND_ID = 6748564450

# === OpenRouter API ===
def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/smartxhacker_bot"
    }
    data = {
        "model": "mistralai/mistral-small-3.2-24b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that always replies in English."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else f"❌ Error: {response.text}"

# === Admin Commands ===
async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return await update.message.reply_text("🚫 You are not authorized.")
    await update.message.reply_text(
        "🛠 Admin Panel\n• /users – Total users\n• /broadcast <message> – Send to all",
        parse_mode="Markdown"
    )

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return await update.message.reply_text("🚫 Not authorized.")
    await update.message.reply_text(f"👥 Total users: {len(users)}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return await update.message.reply_text("🚫 Not authorized.")
    msg = " ".join(context.args)
    if not msg:
        return await update.message.reply_text("⚠️ Usage: /broadcast <message>")
    count = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg)
            count += 1
        except:
            pass
    await update.message.reply_text(f"✅ Message sent to {count} users.")

# === Static Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to SmartxHacker Bot!\nAsk me anything...", reply_markup=ReplyKeyboardRemove())

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Download Smart Tunnel App:\nhttps://smarttunnel.in/smarttunnel.apk")

async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌐 Visit official site:\nhttps://smarttunnel.in")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📬 Message SmartxHacker:\nhttps://t.me/smartxhacker")

# === Message Handler ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    users.add(update.effective_user.id)

    greetings = ["hello", "hi", "hey", "heyy", "hii", "sun", "suno"]
    first_word = user_input.split()[0]
    if update.effective_user.id == GIRLFRIEND_ID and first_word in greetings:
        return await update.message.reply_text("Hello Mrs.Ansari, kaisi hain aap? ✨ Kuch help chahiye aapko? 🎀")

    if any(kw in user_input for kw in ["who is falak", "falak kon hai", "falak kaun hai", "tell me about falak", "who's falak"]):
        return await update.message.reply_text("💖 Falak is the most favorite person of my master. He truly loves her a lot.")

    if any(kw in user_input for kw in ["where is your master", "where is your creator", "where is your boss", "where is your owner",
        "where is he", "where is sir", "where is your sir", "where is farhan", "where is your king", "farhan kahan hai", "wo kya kr rha h"]):
        replies = [
            "👑 He's hiding from bugs... last seen debugging in a cave.",
            "🕶️ My boss? Probably sipping coffee while I do all the work!",
            "💻 Farhan Ansari? Probably taking a nap 🙂",
            "📡 My master is currently offline. Please try again after charging him.",
            "👨‍💻 I'm basically a smart parrot built by Farhan Ansari. Blame him!",
            "📬 [Click here to message your overlord](https://t.me/smartxhacker) 😎"
        ]
        return await update.message.reply_text(random.choice(replies), parse_mode="Markdown")

    if any(kw in user_input for kw in [
        "when he will come online", "kab online aayega", "he is offline", "when will he come", "he will come online", "he is not online", "is he online", "he's offline", "he is not available"
    ]):
        return await update.message.reply_text("💤 He's probably coding in his dreams... He'll be back when the stars align. 🌌")

    if "introduce yourself" in user_input:
        return await update.message.reply_text("I'm SmartxHacker's Assistant, created to help with questions, problems, learning, or just chatting! ✨")

    if "download app" in user_input:
        return await update.message.reply_text("📥 Download Smart Tunnel App:\nhttps://smarttunnel.in/smarttunnel.apk")

    if "official website" in user_input:
        return await update.message.reply_text("🌐 Visit official site:\nhttps://smarttunnel.in")

    if "contact smartxhacker" in user_input:
        return await update.message.reply_text("📬 Message SmartxHacker:\nhttps://t.me/smartxhacker")

    if any(kw in user_input for kw in ["smart tunnel", "smart tunnel app", "download tunnel"]):
        return await update.message.reply_text("📥 Download Smart Tunnel App:\nhttps://smarttunnel.in/smarttunnel.apk")

    if any(kw in user_input for kw in ["who is your master", "who is your creator", "who is your owner", "your master",
        "your creator", "your boss", "your owner", "who made you", "who created you"]):
        return await update.message.reply_text("👑 My master is Farhan Ansari\n📬 [Click to Message](https://t.me/smartxhacker)", parse_mode="Markdown")

    if any(kw in user_input for kw in [
        "who is smartxhacker", "smartxhacker kaun hai", "tell me about smartxhacker", "smartxhacker kon hai"
    ]):
        await update.message.reply_text(
            "👨‍💻 *SmartxHacker* is a tech enthusiast, developer, and the creator of this bot! \n"
            "📬 Contact him directly on Telegram: [Click Here](https://t.me/smartxhacker)",
            parse_mode="Markdown"
        )
        return

    if "farhan" in user_input:
        return await update.message.reply_text("📬 Contact Farhan Ansari:\n[Click to Message](https://t.me/smartxhacker)", parse_mode="Markdown")

    match = re.search(r"\b(i am|i'm)\s+(\w+)", user_input)
    if match:
        person_name = match.group(2).capitalize()
        custom_replies = {
            "Farhan": "Hello Sir, Welcome 😎",
            "Krishna": "Hello Krishna! Welcome to the bot.",
            "Falak": "Hello Mrs. Ansari, how are you? Are you looking for my Master?"
        }
        return await update.message.reply_text(custom_replies.get(person_name, f"Hello {person_name}, nice to meet you!"))

    # Fallback to OpenRouter AI
    reply = ask_openrouter(user_input)
    await update.message.reply_text(reply)

# === Main Entry ===
def run_flask():
    app.run(host="0.0.0.0", port=8080)

def main():
    logging.basicConfig(level=logging.INFO)

    # Start Flask in background thread
    threading.Thread(target=run_flask).start()

    # Create application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_menu))
    application.add_handler(CommandHandler("users", list_users))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("download", download))
    application.add_handler(CommandHandler("website", website))
    application.add_handler(CommandHandler("contact", contact))

    # Text Message Handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
