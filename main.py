import argparse
from pyrogram import Client
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MINUTES = 60
HOURS = 60 * MINUTES

# List of accounts with their corresponding session names
accounts = [
    {
        "session_name": "account1",
        "chat_id": -1001215108117  # Replace with the desired chat ID for this account
    },
    {
        "session_name": "account2",
        "chat_id": -1001215108117  # Replace with the desired chat ID for this account
    },
    {
        "session_name": "account3",
        "chat_id": -1001215108117  # Replace with the desired chat ID for this account
    }
]

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--test", action="store_true",
                    help="Send 'ping' to the chat for all accounts")
args = parser.parse_args()


async def establish_session(session_name, app_id, api_hash):
    async with Client(session_name, app_id, api_hash) as app:
        print(f"Session established for {session_name}!")

# Establish sessions for each account
for account in accounts:
    asyncio.get_event_loop().run_until_complete(
        establish_session(account["session_name"], os.getenv(
            "APP_ID"), os.getenv("API_HASH"))
    )


async def main(session_name, chat_id):
    async with Client(session_name, os.getenv("APP_ID"), os.getenv("API_HASH")) as app:
        print(f"Bot started for {session_name}!")

        if args.test:
            await app.send_message(chat_id, "ping")
            print(f"Account {session_name}: Ping sent!")
            return

        start_hours = 0
        start_minutes = 0
        start_hours = input("Start in (hours) (default: 0): ")
        start_minutes = input("Start in (minutes) (default: 0): ")

        for i in range(int(start_hours) * HOURS + int(start_minutes) * MINUTES, 0, -1):
            print(
                f"Account {session_name}: Time left - {i // HOURS:02d}:{i // MINUTES % 60:02d}:{i % MINUTES:02d}",
                end="\r",
                flush=True,
            )
            await asyncio.sleep(1)

        while True:
            await app.send_message(chat_id, "/harvest")
            await app.send_message(chat_id, "/plant eggplant 9")
            print(f"Account {session_name}: Message sent!")
            await asyncio.sleep(int(6 * HOURS + 5))

# Run the main function for each account
for account in accounts:
    asyncio.get_event_loop().create_task(
        main(account["session_name"], account["chat_id"]))

# Run until the program is closed
asyncio.get_event_loop().run_forever()
