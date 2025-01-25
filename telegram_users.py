import json
import os


class TelegramUsers:
    def __init__(self):
        self.TELEGRAM_USERS_FILE = os.environ.get('TELEGRAM_USERS_FILE')

    def notify_about_keygen(self, chat_id, keyname, message):
        notify_id = chat_id or 0
        notify_username = message.chat.username or message.from_user.username or "unknown_username"
        notify_first_name = message.from_user.first_name or "unknown_first_name"
        notify_last_name = message.from_user.last_name or "unknown_last_name"
        notify_filename = keyname or "unknown_keyname"

        users = self.__load_users()
        for user in users:
            if user['id'] == notify_id:
                return

        print(f"[TelegramUsers.notify_about_keygen] Add new user: "
              f"id={notify_id}, username={notify_username}, "
              f"first_name={notify_first_name}, last_name={notify_last_name}, keyname={notify_filename}")
        users.append({"id": notify_id, "username": notify_username,
                      "first_name": notify_first_name, "last_name": notify_last_name, "keyname": notify_filename})
        self.__save_users(users)

    def get_keyname(self, chat_id):
        users = self.__load_users()
        for user in users:
            if user['id'] == chat_id:
                return user['keyname']
        return None

    def get_all_ids(self):
        users = self.__load_users()
        return [user['id'] for user in users]

    def __load_users(self):
        if not os.path.exists(self.TELEGRAM_USERS_FILE):
            return []
        with open(self.TELEGRAM_USERS_FILE, "r") as file:
            return json.load(file)

    def __save_users(self, users):
        with open(self.TELEGRAM_USERS_FILE, "w") as file:
            json.dump(users, file)
