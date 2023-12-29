from pyrogram import Client
from utils.constants import api_id, api_hash, config


def send_message(account, recipient, message):
    client = Client(
        account,
        api_id=api_id,
        api_hash=api_hash
    )
    client.start()
    client.send_message(recipient, message)
    client.stop()
