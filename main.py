import telebot
import json
import time
import urllib.request

bot = telebot.TeleBot('1313886568:AAGd7Nqy8qDB7zPi198jYMyAX7NBnWW0TU0')
api_key = "6xDCUkjwOaOCkGmHXdogR8rZSXwRn2at"
city_id = "296629"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Для получения прогноза на ближайшие 5 дней отправь мне дату в виде \"07-26\"")


@bot.message_handler(content_types=['text'])
def get_forecast(message):
    daily_forecast_url = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + city_id \
                       + "?apikey=" + api_key \
                       + "&language=ru-ru&details=true&metric=true"
    response = ""
    with urllib.request.urlopen(daily_forecast_url) as daily_forecast_url:
        data = json.loads(daily_forecast_url.read().decode())
        for key in data['DailyForecasts']:
            if str(key['Date']).find(str(message.text)) != -1:
                response += "Прогноз погоды на " + key['Date'] + '\n'
                response += "Минимальная температура: " + str(key['Temperature']['Minimum']['Value']) + '°C\n' \
                            + "Максимальная температура: " + str(key['Temperature']['Maximum']['Value']) + '°C\n' \
                            + str(key['Day']['LongPhrase'])
    if response != "":
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Что-то не так с сервером")


if __name__ == '__main__':
    bot.polling(none_stop=True)
