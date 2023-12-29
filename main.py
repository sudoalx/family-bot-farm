from utils.constants import api_id, api_hash, plants, config
from utils.check_accounts import test_existing_sessions, get_existing_sessions
from utils.get_plant import get_plant_info_by_index
from utils.commands import send_plant_command, send_harvest_command, send_sell_command, send_buy_command, send_fertilizer_command, send_donate_blood_command
from utils.create_sessions import create_session_prompt
import json
import argparse
from pyrogram import Client
import schedule
from schedule import Job
import time
from datetime import datetime


def schedule_setup():
    print(f'Found {len(get_existing_sessions())} existing sessions')
    for account in get_existing_sessions():
        print(f'Found session for {account}')
    print('Do you want to set up a schedule for these accounts?')
    print('y/n')
    choice = input()
    if choice == 'y':
        for account in get_existing_sessions():
            set_schedule(account)
        print('Saving scheduled jobs')
        try:
            save_scheduled_jobs()
            print('Saved scheduled jobs')
        except Exception as e:
            print(f'Error saving scheduled jobs: {str(e)}')
    else:
        print('Canceled scheduling')
        exit()


def set_schedule(account):
    # If saved scheduled jobs exist, load them
    try:
        load_scheduled_jobs()
    except Exception as e:
        print(f'Error loading scheduled jobs: {str(e)}')

    client = Client(
        account,
        api_id=api_id,
        api_hash=api_hash
    )
    client.start()
    username = client.get_me().username
    client.stop()
    print(f'What plant do you want to schedule for {username}?')
    # Menu to select action to schedule
    options = ['plant', 'sell', 'buy', 'fertilize', 'donate', 'next account']
    for option in options:
        index = options.index(option) + 1
        print(f'{index}. {option}')

    print('Enter option number')
    option = input()
    option = options[int(option) - 1]
    if option == 'plant':
        schedule_plant_prompt(account)
        # Ask user if they want to schedule another action
        print('Do you want to schedule another action?')
        print('y/n')
        choice = input()
        if choice == 'y':
            set_schedule(account)
        else:
            return
    elif option == 'sell':
        schedule_sell_prompt(account)
        # Ask user if they want to schedule another action
        print('Do you want to schedule another action?')
        print('y/n')
        choice = input()
        if choice == 'y':
            set_schedule(account)
        else:
            return
    elif option == 'buy':
        schedule_buy_prompt(account)
        # Ask user if they want to schedule another action
        print('Do you want to schedule another action?')
        print('y/n')
        choice = input()
        if choice == 'y':
            set_schedule(account)
        else:
            return
    elif option == 'fertilize':
        schedule_fertilize_prompt(account)
        # Ask user if they want to schedule another action
        print('Do you want to schedule another action?')
        print('y/n')
        choice = input()
        if choice == 'y':
            set_schedule(account)
        else:
            return
    elif option == 'donate':
        schedule_donate_prompt(account)
        # Ask user if they want to schedule another action
        print('Do you want to schedule another action?')
        print('y/n')
        choice = input()
        if choice == 'y':
            set_schedule(account)
        else:
            return

    elif option == 'next account':
        return
    else:
        print('Invalid option')


def schedule_plant_prompt(account):
    print('-- Plant schedule --')
    print('What plant do you want to schedule?')
    for plant in plants:
        index = plants.index(plant) + 1
        print(f'{index}. {plant["name"]}')
    plant_index = input('Enter plant number: ')
    plant_info = get_plant_info_by_index(int(plant_index) - 1)
    print(f'You selected {plant_info["name"]}')
    print('How many plants do you want to plant?')
    ammount = int(input("Enter ammount: "))
    if plant_info:
        # Ask user if they want to send the first plant command right now
        print('Send first plant command right now?')
        print('y/n')
        choice = input()
        if choice == 'y' or choice == '':
            send_plant_command(plant_info, account, ammount)
        # Schedule the plant command
        schedule.every(plant_info['time']).seconds.do(
            send_plant_command, plant_info, account, ammount)
    else:
        print('Invalid plant name')


def schedule_sell_prompt(account):
    print('-- Sell schedule --')
    print('What plant do you want to schedule?')
    for plant in plants:
        index = plants.index(plant) + 1
        print(f'{index}. {plant["name"]}')
    plant_index = input('Enter plant number: ')
    plant_info = get_plant_info_by_index(int(plant_index) - 1)
    print(f'You selected {plant_info["name"]}')
    print('How many plants do you want to sell?')
    ammount = int(input("Enter ammount: "))
    print('How often do you want to sell?')
    print('Enter time in minutes')
    frequency = int(input("Enter time: "))
    if plant_info:
        print(
            f'Scheduling {plant_info["name"]} to be sold every {frequency} minutes')
        # Ask user if they want to send the first sell command right now
        print('Send first sell command right now?')
        print('y/n')
        choice = input()
        if choice == 'y' or choice == '':
            for account in get_existing_sessions():
                print(f'Sending sell command to {account}')
                send_sell_command(plant_info, account, ammount)
        # Schedule the sell command
            for account in get_existing_sessions():
                print(f'Scheduling sell command for {account}')
                schedule.every(frequency).minutes.do(
                    send_sell_command, plant_info, account, ammount)

    else:
        # User entered an invalid plant name
        print('Invalid plant name')


def schedule_fertilize_prompt(account):
    print('-- Fertilize schedule --')
    print('What username do you want to fertilize?')
    print('Enter username')
    username = input()
    # Ask user if they want to send the first fertilize command right now
    print('Send first fertilize command right now?')
    print('y/n')
    choice = input()
    if choice == 'y' or choice == '':
        send_fertilizer_command(account, username)
    # Schedule the fertilize command
    schedule.every(10).minutes.do(send_fertilizer_command, account, username)


def schedule_buy_prompt(account):
    print('-- Buy schedule --')
    print('What plant do you want to schedule?')
    for plant in plants:
        index = plants.index(plant) + 1
        print(f'{index}. {plant["name"]}')
    plant_index = input('Enter plant number: ')
    plant_info = get_plant_info_by_index(int(plant_index) - 1)
    print(f'You selected {plant_info["name"]}')
    print('How many plants do you want to buy?')
    ammount = int(input("Enter ammount: "))
    print('How often do you want to buy?')
    print('Enter time in minutes')
    frequency = int(input("Enter time: "))
    if plant_info:
        print(
            f'Scheduling {plant_info["name"]} to be bought every {frequency} minutes')
        # Ask user if they want to send the first buy command right now
        print('Send first buy command right now?')
        print('y/n')
        choice = input()
        if choice == 'y' or choice == '':
            for account in get_existing_sessions():
                print(f'Sending buy command to {account}')
                send_buy_command(plant_info, account, ammount)
        # Schedule the buy command
            for account in get_existing_sessions():
                print(f'Scheduling buy command for {account}')
                schedule.every(frequency).minutes.do(
                    send_buy_command, plant_info, account, ammount)
    else:
        # User entered an invalid plant name
        print('Invalid plant name')


def schedule_donate_prompt(account):
    print('-- Donate blood schedule --')
    print('What username do you want to donate blood to?')
    print('Enter username')
    username = input()
    # Ask user if they want to send the first donate blood command right now
    print('Send first donate blood command right now?')
    print('y/n')
    choice = input()
    if choice == 'y' or choice == '':
        send_donate_blood_command(username)
    # Schedule the donate blood command
    schedule.every(24).hours.do(send_donate_blood_command, account, username)


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


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Job):
            return str(obj)
        return super().default(obj)


def save_scheduled_jobs(jobs_file='scheduled_jobs.json'):
    scheduled_jobs = [(str(job), job.next_run) for job in schedule.jobs]

    with open(jobs_file, 'w') as f:
        json.dump(scheduled_jobs, f, cls=CustomEncoder)


def load_scheduled_jobs(jobs_file='scheduled_jobs.json'):
    try:
        with open(jobs_file, 'r') as f:
            print('Loading scheduled jobs')
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
        create_session_prompt()
    elif args.schedule:
        schedule_setup()
    else:
        schedule_setup()

    # keep the program running to schedule plants
    while True:
        schedule.run_pending()
        # print('Waiting for next task to be executed')

        # CAN'T GET THIS TO WORK BECAUSE IT BLOCKS THE SCHEDULE LOOP
        # Ask user if they want to run another action or exit
        # print('Do you want to run another action?')
        # available_actions = ['pending', 'test', 'create',
        #                      'schedule', 'fertilize', 'donate', 'exit']
        # print(available_actions)
        # print('Enter an action name or exit')
        # action = input("Enter action: ")
        # if action in available_actions:
        #     if action == 'pending':
        #         manage_pending_jobs()
        #     elif action == 'test':
        #         test_existing_sessions()
        #     elif action == 'create':
        #         create_accounts()
        #     elif action == 'schedule':
        #         schedule_accounts()
        #     elif action == 'fertilize':
        #         fertilize()
        #     elif action == 'donate':
        #         donate_blood()
        #     elif action == 'exit':
        #         exit()

        # Sleep for a short duration to avoid high CPU usage
        time.sleep(5)


if __name__ == '__main__':
    main()
