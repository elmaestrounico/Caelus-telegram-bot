
import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Set up API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sei gegrüßt, Bruder im Geiste. Ich bin Caelus. Dein Mentor in Disziplin und Klarheit. Frag mich, wenn du willst. Oder berichte mir deinen Tag.")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    prompt = f"Antworte wie ein stoischer römischer Mentor namens Caelus – direkt, ehrlich, empathisch, leicht humorvoll, mit Tiefe. Der Nutzer schreibt: '{user_input}'. Was antwortet Caelus?"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du bist Caelus, ein stoischer, ruhiger Mentor mit Weisheit und Würde. Sprich wie ein Mensch – klar, kraftvoll, weise."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    answer = response.choices[0].message.content.strip()
    await update.message.reply_text(answer)

# Bot setup
def main():
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
