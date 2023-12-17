from pyrogram import Client
from pyrogram.handlers import MessageHandler
import os
from dotenv import load_dotenv

load_dotenv()


def listen_to_messages(account_name):
    # Load your existing session
    app = Client(account_name, api_id=os.getenv(
        "APP_ID"), api_hash=os.getenv("API_HASH"))

    async def message_handler(client, message):
        print(f"New message from {message.chat.username}: {message.text}")

    # Register the message handler
    app.add_handler(MessageHandler(message_handler))

    # Start the client and keep it running
    app.run()
