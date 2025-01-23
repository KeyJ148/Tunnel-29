import telebot
import os
import traceback
from telebot import types


class TelegramBot:
    def __init__(self, generate_key_func, get_all_keys_func):
        self.TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
        self.TELEGRAM_PASSWORD = os.environ.get('TELEGRAM_PASSWORD')
        self.TELEGRAM_MESSAGE_INFO = os.environ.get('TELEGRAM_MESSAGE_INFO')
        self.TELEGRAM_MESSAGE_HELLO = os.environ.get('TELEGRAM_MESSAGE_HELLO')
        self.TELEGRAM_MESSAGE_REQUEST_PASSWORD = os.environ.get('TELEGRAM_MESSAGE_REQUEST_PASSWORD')
        self.TELEGRAM_MESSAGE_RIGHT_PASSWORD = os.environ.get('TELEGRAM_MESSAGE_RIGHT_PASSWORD')
        self.TELEGRAM_MESSAGE_WRONG_PASSWORD = os.environ.get('TELEGRAM_MESSAGE_WRONG_PASSWORD')
        self.TELEGRAM_MESSAGE_ZERO_KEYS = os.environ.get('TELEGRAM_MESSAGE_ZERO_KEYS')
        self.TELEGRAM_BUTTON_INFO = os.environ.get('TELEGRAM_BUTTON_INFO')
        self.TELEGRAM_BUTTON_GEN = os.environ.get('TELEGRAM_BUTTON_GEN')
        self.TELEGRAM_BUTTON_ALL_KEYS = os.environ.get('TELEGRAM_BUTTON_ALL_KEYS')

        self.BUTTONS = [self.TELEGRAM_BUTTON_INFO, self.TELEGRAM_BUTTON_GEN, self.TELEGRAM_BUTTON_ALL_KEYS]

        self.bot = telebot.TeleBot(self.TELEGRAM_TOKEN)
        self.generate_key_func = generate_key_func
        self.get_all_keys_func = get_all_keys_func

        self.bot.message_handler(commands=['start'])(self.start_handler)
        self.bot.message_handler(content_types=['text'])(self.all_text_handler)

    def start_handler(self, message):
        print(f"[TelegramBot.start_handler] Request: {str(message)}")
        self.send_message(message.chat.id, self.TELEGRAM_MESSAGE_HELLO, self.BUTTONS)

    def all_text_handler(self, message):
        print(f"[TelegramBot.all_text_handler] Request: {str(message)}")
        if message.text == self.TELEGRAM_BUTTON_INFO:
            self.info_handler(message)
        elif message.text == self.TELEGRAM_BUTTON_GEN:
            self.generate_handler(message)
        elif message.text == self.TELEGRAM_BUTTON_ALL_KEYS:
            self.all_keys_handler(message)
        elif message.text == self.TELEGRAM_PASSWORD:
            self.password_handler(message)

    def info_handler(self, message):
        print(f"[TelegramBot.info_handler] Request: {str(message)}")
        self.send_message(message.chat.id, self.TELEGRAM_MESSAGE_INFO, self.BUTTONS)

    def generate_handler(self, message):
        print(f"[TelegramBot.generate_handler] Request: {str(message)}")
        self.send_message(message.chat.id, self.TELEGRAM_MESSAGE_REQUEST_PASSWORD, self.BUTTONS)
        self.bot.register_next_step_handler(message, self.password_handler)

    def all_keys_handler(self, message):
        keys = self.get_all_keys_func(message)
        if keys is None or len(keys) == 0:
            self.send_message(message.chat.id, self.TELEGRAM_MESSAGE_ZERO_KEYS)
        for key in keys:
            self.send_key(message.chat.id, key)

    def password_handler(self, message):
        print(f"[TelegramBot.password_handler] Request: {str(message)}")
        if message.text == self.TELEGRAM_BUTTON_INFO:
            self.info_handler(message)
        elif message.text.lower() == self.TELEGRAM_PASSWORD.lower():
            self.send_message(message.chat.id, self.TELEGRAM_MESSAGE_RIGHT_PASSWORD, self.BUTTONS)
            key = self.generate_key_func(message)
            self.send_key(message.chat.id, key)
        else:
            self.send_message(message.chat.id, self.TELEGRAM_MESSAGE_WRONG_PASSWORD, self.BUTTONS)
            self.bot.register_next_step_handler(message, self.password_handler)

    def send_key(self, chat_id, key):
        self.send_document(chat_id, key['conf'], key['conf'].name)
        self.send_document(chat_id, key['qr'], key['qr'].name)

    def send_message(self, chat_id, answer_text, buttons=None):
        print(f"[TelegramBot.send_message] Response: text={answer_text}, buttons={buttons}")
        if buttons:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*buttons)
            self.bot.send_message(chat_id, text=answer_text, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=keyboard)
        else:
            self.bot.send_message(chat_id, text=answer_text, parse_mode="Markdown", disable_web_page_preview=True)

    def send_document(self, chat_id, file, filename):
        self.bot.send_document(chat_id, file, visible_file_name=filename)

    def send_photo(self, chat_id, file, caption):
        self.bot.send_photo(chat_id, file, caption=caption)

    def start(self):
        print("[TelegramBot.start] Start...")
        while True:
            try:
                print("[TelegramBot.start] Polling...")
                self.bot.polling(none_stop=True, interval=0)
            except Exception as e:
                print("[TelegramBot.start] Error while polling: " + str(e))
                traceback.print_exc()
