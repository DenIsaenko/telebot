from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def user_contact():
    markup = ReplyKeyboardMarkup(True, True)
    markup.add(KeyboardButton('Отправить контакт', request_contact=True))
    return markup
