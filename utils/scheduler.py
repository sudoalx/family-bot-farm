import schedule
import time


def send_message(message):
    print(message)  # Replace this with your actual code to send the message


def schedule_message(message, delay):
    schedule.every(delay).seconds.do(send_message, message)
    while True:
        schedule.run_pending()
        time.sleep(1)
