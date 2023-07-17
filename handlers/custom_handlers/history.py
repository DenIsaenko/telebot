import json
import os.path

from database.read_write.read_write_func import read_func
from loader import bot

@bot.message_handler(commands=['history'])
def reading_history(message):
    data = read_func(os.path.abspath(f'{message.from_user.id}.json'))
    bot.send_message(message.from_user.id, 'Вы искали: ')
    for key, val in data.items():
        bot.send_message(message.from_user.id, key)
        for j in val:
            bot.send_message(message.from_user.id, j[0])
