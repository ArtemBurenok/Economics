import telebot
from StockTelegramBot import Portfolio

token = ""
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Напиши привет и следуй инструкции.+")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == "Привет":
        bot.reply_to(message, "Привет, введи тикеры компаний, которые тебя интересуют, если акции российские, то "
                              "введи в таком формате: SBER.ME.\n Пример сообщения: SBER.ME, GAZP.ME, AFLT.ME, ROSN.ME")
    elif message.text == "Пока":
        bot.reply_to(message, "Пока")
    else:
        replace = message.text.replace(",", "")
        tickers = replace.split()

        portfolio = Portfolio(tickers)
        share = portfolio.ReturnPortfolio()

        bot.reply_to(message, str(share))


bot.polling()