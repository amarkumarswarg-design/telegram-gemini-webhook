import os
import google.generativeai as genai
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ready hai (FREE webhook).")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = model.generate_content(update.message.text)
        await update.message.reply_text(res.text)
    except:
        await update.message.reply_text("Error aaya.")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot running"

if __name__ == "__main__":
    telegram_app.initialize()
    telegram_app.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
