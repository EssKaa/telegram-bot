from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user.username

    requests.post(N8N_WEBHOOK, json={
        "text": text,
        "user": user
    })

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
