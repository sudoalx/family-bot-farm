from pyrogram import Client
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

APP_ID = os.getenv("APP_ID")
API_HASH = os.getenv("API_HASH")

MINUTES = 60
HOURS = 60 * MINUTES


async def main():
    print(API_HASH, APP_ID)
    async with Client("my_account", APP_ID, API_HASH) as app:
        print("Bot started!")
        # default values
        start_hours = 0
        start_minutes = 0
        # ask when to send the first message
        start_hours = input("Start in (hours) (default: 0): ")
        start_minutes = input("Start in (minutes) (default: 0): ")
        # wait until the time is up and print countdown every second format HH:MM:SS
        for i in range(int(start_hours) * HOURS + int(start_minutes) * MINUTES, 0, -1):
            print(
                # pretty print the time left
                f"{i // HOURS:02d}:{i // MINUTES % 60:02d}:{i % MINUTES:02d}",
                end="\r",
                flush=True,
            )
            await asyncio.sleep(1)
        while True:
            await app.send_message(-1001215108117, "/harvest")
            await app.send_message(-1001215108117, "/plant eggplant 9")
            print("Message sent!")
            await asyncio.sleep(int(6 * HOURS + 5))

# keep running until the program is closed
asyncio.get_event_loop().run_until_complete(main())
