from http import HTTPStatus

import requests
from telegram import ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater
)

from config import TOKEN, WEATHER_URL


def start_bot(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        'Привет! Я могу рассказать тебе о погоде в любом городе мира. '
        'Отправь название этого города, например, <code>Москва</code>',
        parse_mode=ParseMode.HTML
    )
    return 'weather'


def send_weather(update: Update, context: CallbackContext) -> str:
    weather_message = _get_weather(update.message.text)
    update.message.reply_text(weather_message)
    return 'weather'


def get_weather_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('start', start_bot)],
        states={'weather': [MessageHandler(Filters.text, send_weather)]},
        fallbacks=[],
        allow_reentry=True
    )


def _get_weather(city: str) -> str:
    response = requests.get(WEATHER_URL.format(city=city)).json()
    if response['cod'] != HTTPStatus.OK:
        return 'Город не найден'
    temperature = round(response['main']['temp'])
    weather_description = response['weather'][0]['description']
    return f'{city}, {weather_description}, температура {temperature}°C'


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    weather_handler = get_weather_handler()

    dispatcher.add_handler(weather_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
