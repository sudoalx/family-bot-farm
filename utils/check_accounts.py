from utils.constants import api_id, api_hash
from pyrogram import Client
import os


def test_existing_sessions():
    print('Testing existing sessions')
    sessions = get_existing_sessions()
    for session in sessions:
        check_account(session)


def get_existing_sessions():
    sessions = [file.split('.')[0]
                for file in os.listdir() if file.endswith('.session')]
    print(f'Found {len(sessions)} existing sessions')
    return sessions


def check_account(account):
    print(f'Checking account {account}')
    try:
        client = Client(
            account,
            api_id=api_id,
            api_hash=api_hash
        )
        client.start()
        username = client.get_me().username
        print(f'Account with username {username} is working')
        client.stop()
    except Exception as e:
        print(f'Error checking account {account}: {str(e)}')
