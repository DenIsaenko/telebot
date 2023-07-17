
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def button_operation():
    markup = ReplyKeyboardMarkup(True, True)
    low = KeyboardButton(text='Низ->Верх')
    heigh= KeyboardButton(text='Верх->Низ')
    markup.add(low, heigh)
    return markup
def best_prod():
    markup = ReplyKeyboardMarkup(True,True)
    best = KeyboardButton(text='Лучшее предложение')
    markup.add(best)
    return markup





