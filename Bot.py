# "YOUR_BOT_TOKEN" - obtained from @BotFather
# "YOUR_OWM_TOKEN" - obtained from https://home.openweathermap.org/api_keys

import telebot

bot = telebot.TeleBot("YOUR_BOT_TOKEN", parse_mode=None)

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict["language"] = "ru"
owm = OWM("YOUR_OWM_TOKEN", config_dict)
mgr = owm.weather_manager()


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Где узнать погоду? Введите название города: ")

@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Я погодный бот. Напиши мне город, а я скажу, какая сейчас там погода.")

@bot.message_handler(content_types=["text"])

def echo_all(message):
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temp = w.temperature("celsius")["temp"]

    answer = "В городе " + message.text + " сейчас " + w.detailed_status + "." + "\n"
    answer += "Температура воздуха: " + str(round(temp)) + " °С." + "\n\n"

    if temp < 10 and temp > 0:
        answer += ("Холодно, оденься потеплее!")
    elif temp < 0 and temp > -10:
        answer += ("Что-то совсем похолодало...")
    elif temp < -10:
        answer += "Брррр! Мороз!"
    elif temp > 10 and temp < 20:
        answer += "На улице тепло, хорошо!)"
    else:
        answer += "Ух, жара!)"
    bot.send_message(message.chat.id, answer)

bot.infinity_polling()
