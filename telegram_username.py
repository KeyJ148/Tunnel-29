import random
from transliterate import translit


def get_transliterate_user_name(message):
    if message.chat.username is not None:
        if __check_valid_user_name(message.chat.username):
            return message.chat.username
        if __check_valid_user_name(__tr(message.chat.username)):
            return __tr(message.chat.username)
    if message.from_user is not None:
        if message.from_user.username is not None:
            if __check_valid_user_name(message.from_user.username):
                return message.from_user.username
            if __check_valid_user_name(__tr(message.from_user.username)):
                return __tr(message.from_user.username)
        if message.from_user.first_name is not None:
            if message.from_user.last_name is not None:
                name = message.from_user.first_name + '-' + message.from_user.last_name
                if __check_valid_user_name(name):
                    return name
                if __check_valid_user_name(__tr(name)):
                    return __tr(name)
            if __check_valid_user_name(message.from_user.first_name):
                return message.from_user.first_name
            if __check_valid_user_name(__tr(message.from_user.first_name)):
                return __tr(message.from_user.first_name)
    return 'unknown_' + str(random.randint(1, pow(2, 31))) + '_'


def __check_valid_user_name(user_name):
    if len(user_name) == 0:
        return False
    if not (('a' <= user_name[0] <= 'z') or ('A' <= user_name[0] <= 'Z') or ('0' <= user_name[0] <= '9')):
        return False
    if not (('a' <= user_name[-1] <= 'z') or ('A' <= user_name[-1] <= 'Z') or ('0' <= user_name[-1] <= '9')):
        return False
    for c in user_name:
        if not (('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9') or c == '-' or c == '_'):
            return False
    return True


def __tr(text):
    return translit(text, 'ru', reversed=True)
