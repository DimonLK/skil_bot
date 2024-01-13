import telebot
from telebot import types

from config import *
from extensions import Converter, APIException

conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for val in exchanges.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))

conv_markup.add(*buttons)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Я ВАС ПРИВЕТСТВУЮ'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Выбор доступной валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Выберите первую валюту конвертции:'
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Выберете вторую валюту конвертации:'
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Выберете сумму для конвертации:'
    bot.send_message(message.chat.id, text)
    bot.register_next_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f'Цена {amount} {base} в {sym} : {new_price}'
        bot.send_message(message.chat.id, text)



bot.polling()