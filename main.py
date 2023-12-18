import json
import argparse
from pyrogram import Client
import asyncio
import os
from dotenv import load_dotenv
import schedule
import time

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


def get_plant_info_by_index(plant_index):
    return plants[plant_index]


def set_chat_id(chat_id):
    config['chat_id'] = chat_id
    with open('config.json', 'w') as f:
        json.dump(config, f)


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


def create_accounts():
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
        index = plants.index(plant) + 1
        print(f'{index}. {plant["name"]}')
    plant_index = input('Enter plant number: ')
    plant_info = get_plant_info_by_index(int(plant_index) - 1)
    print(f'You selected {plant_info["name"]}')
    print('How many plants do you want to plant?')
    ammount = int(input("Enter ammount: "))
    if plant_info:
        schedule_plant(plant_info, account, ammount)
    else:
        print('Invalid plant name')


def schedule_plant(plant_info, account, ammount):
    time = plant_info['time']  # frequency in minutes
    plant_name = plant_info['name']
    print('Sending harvest command to make sure slots are available...')
    send_harvest_command(account)
    print(f'Sending first plant command for {plant_name}...')
    plant(plant_info, account, ammount)
    print(f'Scheduling {plant_name} to be planted every {time/60} minutes')
    schedule.every(time).seconds.do(plant, plant_info, account, ammount)


def plant(plant_info, account, ammount):
    print(f'Planting {plant_info["name"]}...')
    send_plant_command(plant_info, account, ammount)


def send_plant_command(plant_info, account, ammount):
    client = Client(
        account,
        api_id=api_id,
        api_hash=api_hash
    )
    chat_id = config['chat_id']
    plant_command = f'/plant {plant_info["name"]} {ammount}'
    client.start()
    client.send_message(int(chat_id), str(plant_command))
    client.stop()


def send_harvest_command(account):
    client = Client(
        account,
        api_id=api_id,
        api_hash=api_hash
    )
    chat_id = config['chat_id']
    harvest_command = '/harvest'
    client.start()
    client.send_message(int(chat_id), str(harvest_command))
    client.stop()


def schedule_accounts():
    sessions = get_existing_sessions()
    for session in sessions:
        set_schedule(session)


def fertilize():
    print('Set fertilizer every 20 minutes for a specific username')
    print('Enter username')
    username = input()
    schedule.every(20).minutes.do(fertilize_user, username)


def fertilize_user(username):
    print(f'Ferilizing {username}')
    send_fertilizer_command(username)


def send_fertilizer_command(username):
    for account in get_existing_sessions():
        chat_id = config['chat_id']
        client = Client(
            account,
            api_id=api_id,
            api_hash=api_hash
        )
        client.start()
        client.send_message(chat_id, '/fertilize @' + username)
        client.stop()


def donate_blood():
    print('Set donate blood every 24 hours for a specific username')
    print('Enter username')
    username = input()
    schedule.every(24).hours.do(donate_blood_user, username)


def donate_blood_user(username):
    print(f'Donating blood for {username}')
    send_donate_blood_command(username)


def send_donate_blood_command(username):
    for account in get_existing_sessions():
        chat_id = config['chat_id']
        client = Client(
            account,
            api_id=api_id,
            api_hash=api_hash
        )
        client.start()
        client.send_message(chat_id, '/donateblood @' + username)
        client.stop()


def manage_pending_jobs():
    print(schedule.jobs)
    while schedule.jobs:
        options = ['clearall', 'clear', 'exit']
        print('Enter an option')
        print(options)
        option = input()
        if option == 'clearall':
            schedule.clear()
        elif option == 'clear':
            print('Enter job index')
            index = int(input())
            schedule.jobs.pop(index)
        else:
            break


def save_scheduled_jobs(jobs_file='scheduled_jobs.json'):
    scheduled_jobs = [(str(job), job.next_run) for job in schedule.jobs]
    with open(jobs_file, 'w') as f:
        json.dump(scheduled_jobs, f)


def load_scheduled_jobs(jobs_file='scheduled_jobs.json'):
    try:
        with open(jobs_file, 'r') as f:
            scheduled_jobs = json.load(f)
            for job_str, next_run in scheduled_jobs:
                job = eval(job_str)
                job.next_run = next_run
                schedule.jobs.append(job)
    except FileNotFoundError:
        pass  # Ignore if the file doesn't exist


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
        create_accounts()
    elif args.schedule:
        schedule_accounts()
    else:
        schedule_accounts()

    # check if there are pending jobs
    pending_jobs = schedule.jobs

    # keep the program running to schedule plants
    while pending_jobs:
        schedule.run_pending()
        print('Waiting for next task to be executed')
        # Ask user if they want to run another action or exit
        print('Do you want to run another action?')
        available_actions = ['pending', 'test', 'create',
                             'schedule', 'fertilize', 'donate', 'exit']
        print(available_actions)
        print('Enter an action name or exit')
        action = input("Enter action: ")
        if action in available_actions:
            if action == 'pending':
                manage_pending_jobs()
            elif action == 'test':
                test_existing_sessions()
            elif action == 'create':
                create_accounts()
            elif action == 'schedule':
                schedule_accounts()
            elif action == 'fertilize':
                fertilize()
            elif action == 'donate':
                donate_blood()
            elif action == 'exit':
                exit()


if __name__ == '__main__':
    main()
