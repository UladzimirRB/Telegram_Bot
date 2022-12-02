import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, ConvertionException
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help (message):
    text = 'Чтобы конвертировать валюту введите команду в следующем формате: \n\
<валюта которую перевести> <валюта в которую перевести> <количество переводимой валюты> \n\
 Например: доллар евро 100 \n Увидеть список всех доступных валют : /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values (message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types =['text'])
def convert (message):
    try:
        values = message.text.split()
        if len(values) < 3:
            raise ConvertionException ("слишком мало параметров")
        elif len(values) > 3:
            raise ConvertionException("слишком много параметров")

        quote,base,amount = values
        quote = quote.lower()
        base = base.lower()

        summ = CryptoConverter.get_price(quote,base,amount)
    except ConvertionException as e:
        bot.reply_to(message, f"ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"не удалось обработать команду \n {e}")
    else:
        text = f'Стоимость {amount} {keys[quote]} = {summ} {keys[base]}'
        bot.send_message(message.chat.id, text)

bot.polling()
