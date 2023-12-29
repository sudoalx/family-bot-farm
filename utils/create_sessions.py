from utils.constants import api_id, api_hash, config
from utils.check_accounts import get_existing_sessions
from pyrogram import Client


def create_session_prompt():
    if get_existing_sessions():
        print('Existing sessions found, do you want to create new ones?')
        print('y/n')
        choice = input()
        if choice != 'y':
            print('Canceled creating new sessions')
            exit()

    print('How many sessions do you want to create?')
    num_accounts = int(input())

    for i in range(num_accounts):
        print('Enter account name')
        account_name = input()
        create_new_session(account_name)
    print(f'Created {num_accounts} sessions')


def create_new_session(account_name):
    client = Client(
        account_name,
        api_id=api_id,
        api_hash=api_hash
    )
    client.start()
    username = client.get_me().username
    client.stop()
    print(f'Created session for {username}')
