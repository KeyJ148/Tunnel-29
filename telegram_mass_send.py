from telegram_users import TelegramUsers
from telegram import TelegramBot
import os
import json

TELEGRAM_MASS_TEXT_FILE = os.environ.get('TELEGRAM_MASS_TEXT_FILE')

telegram_bot = TelegramBot(None, None)
telegram_users = TelegramUsers()

with open(TELEGRAM_MASS_TEXT_FILE, "r") as file:
    text = file.read()
ids = telegram_users.get_all_ids()

for chat_id in ids:
    telegram_bot.send_message(chat_id, text, None)
