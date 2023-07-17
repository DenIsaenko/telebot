from telebot.handler_backends import State, StatesGroup

class UserInfoProd(StatesGroup):
    name_prod = State()
    sort_product = State()
    best_offer = State()
    cont_ord = State()
    desired_product = State()
    buyer_name = State()
    city = State()
    contact = State()