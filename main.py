import math
import os
import datetime
import requests
import config as cfg
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Пермь", "Гарюшки", "Гайны"]
    keyboard.add(*buttons)
    await message.answer("Где смотрим?", reply_markup=keyboard)

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ru&units=metric&appid=9ad899165d06cc3855e311d7dd523629")

        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, я не понимаю, что там за погода..."

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n" 
            f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n" f"Влажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
            )
    except:
        await message.reply("Проверьте название города!")

if __name__ == "__main__":
    # С помощью метода executor.start_polling опрашиваем
    # Dispatcher: ожидаем команду /start
    executor.start_polling(dp)