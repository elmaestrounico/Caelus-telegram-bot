import logging
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging aktivieren
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Flask App
app = Flask(__name__)

# Token & Webhook-URL aus ENV
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # z. B. https://dein-bot.onrender.com

# Telegram Bot App
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# /start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salve, Bruder im Geiste. Ich bin Caelus – dein Mentor auf dem Pfad zur inneren Stärke.")

application.add_handler(CommandHandler("start", start))

# Webhook Route
@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return 'ok', 200

# Server starten und Webhook setzen
if __name__ == '__main__':
    application.bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}")
    app.run(host='0.0.0.0', port=10000)
