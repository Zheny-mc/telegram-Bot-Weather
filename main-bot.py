from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tokens import bot_token, weather_token
import requests

WEATHER_TOKEN = weather_token()

def get_temp(city: str):
    ''' пример вызова: get_temp(city='Дубай') '''
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}&units=metric')
    if res.status_code == 200:
        data = res.json()
        return data['main']['temp']
    else:
        raise ValueError('A very specific bad thing happened.')

BOT_TOKEN = bot_token()

async def on_startup(_):
    print('Бот вышел в онлайн.')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    text = 'Привет, рад тебя видеть! Напиши напиши название города и получи текущую температуру!'
    await message.answer(text)

@dp.message_handler()
async def view_weather_command(message: types.Message):
    city = message.text.strip().lower()
    try:
        temp = get_temp(city)
        name_img = 'солнечно.jpg' if temp > 23 else 'облачно.jpg'
        file = open(f'img/{name_img}', 'rb')
        await bot.send_photo(message.from_user.id, file, f'Температура в {city}: {temp}')
    except:
        await message.answer('Город не найден.')



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


