from utils.constants import config
from utils.check_accounts import get_existing_sessions
from utils.send_message import send_message


def send_plant_command(plant_info, account, ammount):
    chat_id = config['chat_id']
    plant_command = f'/plant {plant_info["name"]} {ammount}'
    send_harvest_command(account)
    send_message(account, chat_id, plant_command)


def send_harvest_command(account):
    chat_id = config['chat_id']
    harvest_command = '/harvest'
    send_message(account, chat_id, harvest_command)


def send_sell_command(plant_info, account, ammount):
    chat_id = config['chat_id']
    sell_command = f'/sell {plant_info["name"]} {ammount}'
    send_message(account, chat_id, sell_command)


def send_buy_command(plant_info, account, ammount):
    chat_id = config['chat_id']
    buy_command = f'/add {plant_info["name"]} {ammount}'
    send_message(account, chat_id, buy_command)


def send_fertilizer_command(account, username):
    chat_id = config['chat_id']
    fertilize_command = '/fertilize @' + username
    send_message(account, chat_id, fertilize_command)


def send_donate_blood_command(account, username):
    chat_id = config['chat_id']
    donate_blood_command = '/donateblood @' + username
    send_message(account, chat_id, donate_blood_command)
