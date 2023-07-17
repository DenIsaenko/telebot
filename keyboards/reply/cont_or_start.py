from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def cont_start():
    markup = ReplyKeyboardMarkup(True, True)
    con = KeyboardButton('Продолжаем')
    start = KeyboardButton('Ищем ещё')
    markup.add(con, start)
    return markup