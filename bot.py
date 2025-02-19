import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Список доступных валют
CURRENCIES = {
    "евро": "EUR",
    "доллар": "USD",
    "рубль": "RUB",
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = ("Привет! Я бот-конвертер валют.\n"
            "Формат запроса: <валюта 1> <валюта 2> <количество>\n"
            "Например: доллар рубль 100\n"
            "Список доступных валют: /values")
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\n" + "\n".join(CURRENCIES.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        args = message.text.split()

        if len(args) != 3:
            raise APIException("Ошибка: введите данные в формате 'валюта1 валюта2 количество'.")

        base, quote, amount = args

        if base.lower() not in CURRENCIES or quote.lower() not in CURRENCIES:
            raise APIException("Ошибка: одна из валют недоступна. Используйте /values для списка валют.")

        base, quote = CURRENCIES[base.lower()], CURRENCIES[quote.lower()]

        result = CurrencyConverter.get_price(base, quote, amount)
        bot.reply_to(message, result)

    except APIException as e:
        bot.reply_to(message, str(e))
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка: {e}")


bot.polling()
