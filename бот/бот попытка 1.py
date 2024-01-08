
import telebot
from config import keys, TOKEN
from extensions import ConvertException, CriptoConverter


bot = telebot.TeleBot('6679515591:AAEXobvdATaE-LFaiu5aSei-8-89A8qRv-8')


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text1 = ('Добро пожаловать. Данный бот был разработат для конвертирования валюты, в ведите /help  что бы узнать как работает бот' )
    bot.reply_to(message, text1)
@bot.message_handler( commands=['help'])
def help(message: telebot.types.Message):
    text2 = ('Что бы начать работу введите команду боту в следующем формате:\
<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \
Введите /values  что бы узнать какие валюты можно ковертировать')
    bot.reply_to(message, text2)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
        bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
             raise ConvertException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CriptoConverter.convert(quote, base, amount)

    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e} ')
    except Exception as e:
        bot.reply_to(message, f' Не удолось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * float(amount)}'
        bot.send_message(message.chat.id,text)

bot.polling()