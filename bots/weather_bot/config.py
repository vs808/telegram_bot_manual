import os

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')
WEATHER_KEY = os.getenv('WEATHER_KEY')
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid=' + WEATHER_KEY
