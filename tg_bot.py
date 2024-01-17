import telebot
from geopy.geocoders import Nominatim
import requests
from telebot import types

bot = telebot.TeleBot('6771305097:AAFOZuGJfuJAAsGN57p8AEa5SbBxf-JGuSc')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Узнать погоду")
    markup.add(button)
    bot.send_message(message.chat.id, "Нажми кнопку 'Узнать погоду', чтобы узнать прогноз.",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Узнать погоду")
def ask_city(message):
    msg = bot.send_message(message.chat.id, "Введите название города:")
    bot.register_next_step_handler(msg, get)


@bot.message_handler()
def get(message):
    geolocator = Nominatim(user_agent="WeatherApp")
    location = geolocator.geocode(message.text)

    if not location:
        bot.send_message(message.chat.id, 'Нет такого города', parse_mode="html")

    lat, lon = location.latitude, location.longitude

    api_key = 'c3c83c1f-99f1-4940-bc40-1702b21eaacf'
    url = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&extra=true'
    headers = {'X-Yandex-API-Key': api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        bot.send_message(message.chat.id, 'Запрос не удался', parse_mode="html")

    try:
        current_temp = data['fact']['temp']
        pressure_mm = data['fact']['pressure_mm']
        wind_speed = data['fact']['wind_speed']
    except KeyError:
        bot.send_message(message.chat.id, 'Недействительный ответ', parse_mode="html")

    bot.send_message(message.chat.id,
                     f"Температура: {current_temp} \nДавление: {pressure_mm} \nСкорость ветра: {wind_speed}",
                     parse_mode="html")


bot.polling(none_stop=True)
