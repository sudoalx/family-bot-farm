import json
import argparse
from pyrogram import Client
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# get plants from json file
with open('plants.json') as f:
    plants = json.load(f)
print(plants)


def check_account(account):
    print(account)
    client = Client(
        account,
        api_id=api_id,
        api_hash=api_hash
    )
    client.start()
    print(client.get_me().username)
    client.stop()


def get_existing_sessions():
    sessions = [file.split('.')[0]
                for file in os.listdir() if file.endswith('.session')]
    return sessions


def test_existing_sessions():
    sessions = get_existing_sessions()
    for session in sessions:
        check_account(session)


def check_existing_accounts_json():
    with open('accounts.json') as f:
        accounts = json.load(f)
    for account in accounts:
        check_account(account)


def create_new_session(account):
    client = Client(
        account,
        api_id=api_id,
        api_hash=api_hash
    )
    client.start()
    print(client.get_me().username)
    client.stop()


def init_bot():
    print('How many accounts do you want to create?')
    num_accounts = int(input())
    accounts = []
    for i in range(num_accounts):
        print('Enter account name')
        account = input()
        accounts.append(account)
        create_new_session(account)
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f)
    print(f'Created {num_accounts} accounts')
