from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message:
        return

    text = message.text

    user = message.from_user
    username = user.username or user.first_name

    chat_id = message.chat_id

    # 👉 an n8n senden
    try:
        requests.post(N8N_WEBHOOK, json={
            "text": text,
            "user": username,
            "chat_id": chat_id
        })
    except Exception as e:
        print("Fehler beim Senden an n8n:", e)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot läuft...")
    app.run_polling()
