import json
import argparse
from pyrogram import Client
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# get plants info from json file
with open('plants.json') as f:
    data = json.load(f)
    plants = data['plants']

with open('config.json') as f:
    config = json.load(f)


def get_plant_info_by_name(plant_name):
    for plant in plants:
        if plant['name'] == plant_name:
            return plant


def set_chat_id(chat_id):
    config['chat_id'] = chat_id
    with open('config.json', 'w') as f:
        json.dump(config, f)


def check_account(account):
    print(f'Checking account {account}')
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
    print(f'Found {len(sessions)} existing sessions')
    return sessions


def test_existing_sessions():
    print('Testing existing sessions')
    sessions = get_existing_sessions()
    for session in sessions:
        check_account(session)


def create_new_session(account):
    client = Client(
        account,
        api_id=api_id,
        api_hash=api_hash
    )
    client.start()
    print(client.get_me().username)
    client.stop()


def create_accounts_prompt():
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


def init_bot():
    if get_existing_sessions():
        print('Existing sessions found, do you want to create new ones?')
        print('y/n')
        choice = input()
        if choice == 'y':
            create_accounts_prompt()
    else:
        create_accounts_prompt()


def set_schedule(account):
    client = Client(
        account,
        api_id=api_id,
        api_hash=api_hash
    )
    client.start()
    username = client.get_me().username
    client.stop()
    print(
        f'What plant do you want to schedule for {username}?')
    for plant in plants:
        print(">", plant['name'])
    plant_name = input('Enter plant name: ')
    plant_info = get_plant_info_by_name(plant_name)
    print(plant_info)


def schedule_accounts():
    sessions = get_existing_sessions()
    for session in sessions:
        set_schedule(session)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true',
                        help='Test existing sessions')
    parser.add_argument('-c', '--create', action='store_true',
                        help='Create new sessions')
    parser.add_argument('-s', '--schedule', action='store_true',
                        help='Schedule a plant for an account')
    args = parser.parse_args()
    if args.test:
        test_existing_sessions()
    elif args.create:
        init_bot()
    elif args.schedule:
        schedule_accounts()
    else:
        print('No arguments passed')


if __name__ == '__main__':
    main()
