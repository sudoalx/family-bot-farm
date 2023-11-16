from pyrogram import Client
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Load your existing session
app = Client("account2", api_id=os.getenv("APP_ID"), api_hash=os.getenv("API_HASH"))

# Define a function to handle incoming messages
async def message_handler(client, message):
    print(f"New message from {message.chat.username}: {message.text}")

# Register the message handler
app.add_handler(MessageHandler(message_handler))

# Start the client and keep it running
app.run()
