import telebot

# Импортируем ключ и url API из файла environment.py
from environment import TOKEN
from environment import urlSource
from urllib.parse import urljoin
from telebot import types
import pprint
import requests

bot = telebot.TeleBot(TOKEN)

HOST = 'https://api.telegram.org'
URI = '/bot{token}/{method}'
currency = requests.get(urlSource).json()

@bot.message_handler(commands=['start','help','помогите'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # рисуем кнопки
    itembtn1 = types.KeyboardButton('BTC')
    itembtn2 = types.KeyboardButton('ETH')
    itembtn3 = types.KeyboardButton('ETC')
    itembtn4 = types.KeyboardButton('DOGE')
    itembtn5 = types.KeyboardButton('RVN')
    itembtn6 = types.KeyboardButton('XMR')
    markup.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6)
    msg = bot.send_message(message.chat.id,"Курс какой криптовалюты вас интересует?\n(введите тикер монеты или выберите из предложенных)", reply_markup=markup)
    bot.register_next_step_handler(msg,process_coin_step)

def process_coin_step(message):
    try:
        markup = types.ReplyKeyboardRemove(selective=False)
        # осуществляем выборку монет из словаря currency - туда записан JSON
        for coin in currency['data']:
            if (message.text == coin['symbol'] ):
                bot.send_message(message.chat.id, printCoin(coin['priceUsd'],coin['marketCapUsd']),
                                 reply_markup=markup, parse_mode="Markdown")
    # обработка ошибок
    except Exception as e:
        bot.reply_to(message, 'oooops!')

def printCoin(price, cap):
    # Форматирование и вывод курса пользователю
    return ("Текущая цена, $: " + "{0:.4f}".format(float(str(price))) + "\nРыночная капитализация,$: " + str(int(float(str (cap)))))

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()




