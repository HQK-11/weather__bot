import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

weather_token = '93fcef0e91986f30be7992ed1ae9cc00'

bot = Bot(token='5448676163:AAFhRHaI2D8Kzq_3cwqzIeiCmJYRLIYLm3A')
dp = Dispatcher(bot)

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет, напиши город и я покажу сводку погоды")


# def get_weather(city, weather_token):
@dp.message_handler()
async def get_weather(message: types.message):
    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        humidity = data['main']['humidity']

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        temp = data['main']['temp']
        wind = data['wind']['speed']
        pressure = data['main']['pressure']
        sunrise_timestep = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                             f"Погода в городе: {city}\nТемпература: {temp}C° {wd}\n"
                             f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                             f"Восход солнца: {sunrise_timestep}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                             f"***Хорошего дня!***"
                             )

    except:
        await message.answer("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
