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




# print(currency)
# print(currency['data'][0]['priceUsd'])
# for key in currency['data'][0]:
#    print(key)




# Получение данных о боте

"""def get_me():
    method_name = 'getMe'

    # Просто собираем URL
    url = urljoin(HOST, URI.format(token=TOKEN, method=method_name))
    # Тоже самое что и:
    # url = HOST + URI.format(token=TOKEN, method=method_name)
    print(url)
    #
    response = requests.get(url)
    return response.json()


result = get_me()
pprint.pprint(result)

# 
# Получить все последние сообщения
# 
# def get_updates():
#     method_name = 'getUpdates'
#
#     url = urljoin(HOST, URI.format(token=TOKEN, method=method_name))
#     print(url)
#     response = requests.get(url)
#     return response.json()
#
# result = get_updates()
# pprint.pprint(result)
#
# messages = [m['message']['text'] for m in result['result']]
# pprint.pprint(messages)


# Получаем все обновления с учетом последнего обновления

def get_updates(update_id=None):
    method_name = 'getUpdates'

    url = urljoin(HOST, URI.format(token=TOKEN, method=method_name))
    # print(url)
    if not update_id:
        response = requests.get(url)
    else:
        response = requests.get(url, params={'offset': update_id})
    return response.json()


result = get_updates()
pprint.pprint(result)

last_update_id = result['result'][-1].get('update_id')
print(last_update_id)
result = get_updates(last_update_id + 1)
pprint.pprint(result)

from requests.exceptions import ReadTimeout


# Получаем все последние сообщения с таймаутом

def get_updates(update_id=None):
    method_name = 'getUpdates'

    url = urljoin(HOST, URI.format(token=TOKEN, method=method_name))
    # print(url)
    if not update_id:
        response = requests.get(
            url, params={'timeout': 10}, timeout=10
        )
    else:
        response = requests.get(
            url, params={'offset': update_id, 'timeout': 10}, timeout=10
        )
    return response.json()


# Тело бота (генератор): получаем сообщения и выбрасываем их наружу


def get_messages():
    next_update_id = None
    './file.txt'
    while True:
        try:
            result = get_updates(next_update_id)
        except ReadTimeout:
            continue

        for update in result.get('result', []):
            
            # Роутинг: на какое сообщение как реагировать
            
            if 'message' in update:
                yield update['message']
                if message['text'] == "Привет":
                    answer = yield ("Привет и тебе")
                    print(answer)
                    bot.send_message(chat_id =  516294565, text="Привет и тебе")
                    bot.send_message(chat_id=516294565, text=message['text'])

            elif 'edited_message' in update:
                yield update['edited_message']
            else:
                print('Неизвестный апдейт')

        if result.get('result'):
            
            # сохраняем из последнего сообщения ID апдейта
            # чтобы в следующий раз читать начиная со следующего
            
            next_update_id = result['result'][-1].get('update_id') + 1



for message in get_messages():
    pprint.pprint(message)
    
"""