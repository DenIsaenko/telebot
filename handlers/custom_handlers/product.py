import json


from database.read_write.read_write_func import write_func
import os

from loader import bot
from states.prod_sel import UserInfoProd
from SITE_API.req_api import get_json
from telebot.types import Message
from keyboards.reply.sort_prod import button_operation, best_prod
from keyboards.reply.contact import user_contact
from keyboards.reply.cont_or_start import cont_start
from random import randint


def product_sorting_function(name_prod, reverse=True):
    user_inp = get_json(name_prod)
    resLST = user_inp['result']['resultList']
    titels = list(map(lambda x: (x['item']['title'],
                                 x['item']['itemUrl'],
                                 x['item']['sku']['def']['promotionPrice']), resLST))
    sort_title = sorted(titels, key=lambda i: i[2], reverse=reverse)
    return sort_title



@bot.message_handler(commands=['product'])
def prod_select(message: Message):
    bot.set_state(message.from_user.id, UserInfoProd.name_prod, message.chat.id)
    bot.send_message(message.from_user.id, 'Итак, давай выбирать, что тебя интересует?')



@bot.message_handler(state=UserInfoProd.name_prod)
def search_prod(message: Message):

    bot.send_message(message.from_user.id, f'Значит выбираем {message.text}')
    bot.send_message(message.from_user.id, 'Давай отсортируем по цене.', reply_markup=button_operation())
    bot.set_state(message.from_user.id, UserInfoProd.sort_product, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text



@bot.message_handler(content_types= ['text'], state=UserInfoProd.sort_product)
def sort_prod(message: Message):

    try:
        if message.text == 'Низ->Верх':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                name = data['name']
            sort_myProd = product_sorting_function(name, False)
            prod_hist = {}
            prod_hist[name] = sort_myProd
            write_func(os.path.abspath(f'{message.from_user.id}.json'), prod_hist)

            for i in sort_myProd:
                bot.send_message(message.from_user.id, '\n'.join(i[:2]))


        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                name = data['name']
            sort_myProd = product_sorting_function(name)
            prod_hist = {}
            prod_hist[name] = sort_myProd
            prod_hist[name] = sort_myProd

            write_func(os.path.abspath(f'{message.from_user.id}.json'), prod_hist)

            for i in sort_myProd:
                bot.send_message(message.from_user.id, '\n'.join(i[:2]))

        bot.send_message(message.from_user.id, 'Зацени! Лучшее предложение', reply_markup=best_prod())
        bot.set_state(message.from_user.id, UserInfoProd.best_offer, message.chat.id)
    except KeyError:
        bot.send_message(message.from_user.id, 'Такого нет, напиши что-нибудь нормальное')
        bot.set_state(message.from_user.id, UserInfoProd.name_prod, message.chat.id)



@bot.message_handler(content_types= ['text'], state=UserInfoProd.best_offer)
def selling_prive(message: Message):
    if message.text == 'Лучшее предложение':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            name = data['name']
        user_input = get_json(name)
        resLST = user_input['result']['resultList']
        titels = list(map(lambda x: (x['item']['title'],
                                     x['item']['itemUrl'],
                                     x['item']['sales'] / x['item']['sku']['def']['promotionPrice']), resLST))
        leader = sorted(titels, key=lambda i: i[2], reverse=True)
        bot.send_message(message.from_user.id, '\n'.join(leader[0][:2]))
        bot.send_message(message.from_user.id, 'Будем ёщё что-то заказывать или посмотрим что-то ещё ?\n'
                                               'Если хочешь посмотреть что-то ещё нажми "Ищем ещё",\n'
                                               'а если хочешь продолжить нажми "продолжаем"', reply_markup=cont_start())
        bot.set_state(message.from_user.id, UserInfoProd.cont_ord, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не по плану')
@bot.message_handler(state=UserInfoProd.cont_ord)
def continue_order(message: Message):
    if message.text == 'Продолжаем':
        bot.send_message(message.from_user.id, 'Скопируй и отправь мне полное название товара для заказа')
        bot.set_state(message.from_user.id, UserInfoProd.desired_product, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Что ищем?')
        bot.set_state(message.from_user.id, UserInfoProd.name_prod, message.chat.id)
@bot.message_handler(state=UserInfoProd.desired_product)
def diserd_prod(message: Message):

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        name = data['name']
    user_input = get_json(name)
    resLST = user_input['result']['resultList']
    titles = list(map(lambda x: x['item']['title'], resLST))

    if message.text in titles:
        bot.send_message(message.from_user.id, 'Отлично, записал. Теперь напиши своё имя для заказа.')
        bot.set_state(message.from_user.id, UserInfoProd.buyer_name, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['full_product_name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Видимо ты что-то не так сделал, попробуй еще раз')


@bot.message_handler(state=UserInfoProd.buyer_name)
def get_name(message: Message):
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Записал, теперь пришли мне город в котором ты проживаешь')
        bot.set_state(message.from_user.id, UserInfoProd.city,message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['buyer_name'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Что-то не так! Попробуй ещё раз')
@bot.message_handler(state=UserInfoProd.city)
def get_city(message: Message):
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Отлично. Теперь пришли мне свой номер нажав на кнопку',
                         reply_markup=user_contact())
        bot.set_state(message.from_user.id, UserInfoProd.contact, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Что-то не так! Попробуй ещё раз')

@bot.message_handler(content_types=['text', 'contact'], state=UserInfoProd.contact)
def get_contact(message: Message):
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            text = f'Cпасибо за предоставленную инфорамацию. Ваш заказ:\n' \
                   f'Полное название товара: {data["full_product_name"]}\n' \
                   f'Имя получателя: {data["buyer_name"]}\n' \
                   f'Город: {data["city"]}\n' \
                   f'Номер телефона получателя: {data["phone_number"]}\n' \
                   f'Трек-номер заказа: {randint(1000, 50000)}\n'
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить номер телефона нажмите кнопку')














