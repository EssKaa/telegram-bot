from telethon import TelegramClient, events
import requests
import os
import asyncio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK")

client = TelegramClient("session", API_ID, API_HASH)


@client.on(events.NewMessage)
async def handle_message(event):
    message = event.message

    if not message:
        return

    text = message.message
    if not text:
        return

    sender = await event.get_sender()
    username = getattr(sender, "username", None) or getattr(sender, "first_name", "unknown")

    chat_id = event.chat_id

    # 👉 an n8n senden (gleiches Format!)
    try:
        requests.post(N8N_WEBHOOK, json={
            "text": text,
            "user": username,
            "chat_id": chat_id
        })
    except Exception as e:
        print("error sending to n8n:", e)

async def main():
    while True:
        try:
            print("Starting client...")
            await client.start()
            print("connected")
            await client.run_until_disconnected()
        except Exception as e:
            print("connection lost:", e)
            await asyncio.sleep(5)


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
