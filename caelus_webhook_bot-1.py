
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from flask import Flask, request

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Flask App
app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this to your Render public URL + /webhook

# Application
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salve, Bruder im Geiste. Ich bin Caelus – dein Mentor auf dem Pfad zur inneren Stärke.")

application.add_handler(CommandHandler("start", start))

# Flask Route for Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return 'OK'

# Set webhook when Flask starts
@app.before_request
def init_webhook():
    application.bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
