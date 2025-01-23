from telegram import TelegramBot
from keygen import KeysGenerator
from telegram_username import get_transliterate_user_name
from telegram_users import TelegramUsers


class Tunnel29:
    def __init__(self):
        self.keys_generator = KeysGenerator()
        self.telegram_users = TelegramUsers()
        self.telegram_bot = TelegramBot(self.__generate_key, self.__get_all_keys_func)

    def start(self):
        self.telegram_bot.start()

    def __generate_key(self, message):
        user_name = get_transliterate_user_name(message)
        self.telegram_users.notify_about_keygen(message.chat.id, user_name, message)
        keyname = self.telegram_users.get_keyname(message.chat.id)
        return self.keys_generator.generate_key(keyname)

    def __get_all_keys_func(self, message):
        keyname = self.telegram_users.get_keyname(message.chat.id)
        if keyname is None:
            return []
        return self.keys_generator.get_client_all_keys(keyname)


tunnel29 = Tunnel29()
tunnel29.start()
