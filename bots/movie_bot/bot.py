import os

from dotenv import load_dotenv
from telegram import (
    CallbackQuery,
    ParseMode,
    Update
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Updater
)

from constants import COUNTS_MOVIES, GENRES
from db import get_movies_list
from keyboards import (
    get_keyboard_select_genre,
    get_keyboard_select_others_and_select_genre,
    get_keyboard_with_genres
)
from utils import generate_message_with_movies_list, get_genre


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f'Привет, {update.effective_user.first_name}! '
        'Выбери жанр, и я отправлю тебе несколько случайных фильмов этого жанра',
        reply_markup=get_keyboard_select_genre()
    )


def find_out_genre_of_film(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.reply_text(
        'Выбери один из жанров:',
        reply_markup=get_keyboard_with_genres(GENRES)
    )


def send_movies_list(update: Update, context: CallbackContext) -> None:
    query = _get_query(update)
    selected_genre = query.data
    _send_selected_movies(selected_genre, query)


def send_list_of_other_movies(update: Update, context: CallbackContext) -> None:
    query = _get_query(update)
    selected_genre = query.data.split()[1]
    _send_selected_movies(selected_genre, query)


def _get_query(update: Update) -> CallbackQuery:
    query = update.callback_query
    query.answer()
    return query


def _send_selected_movies(selected_genre: str, query: CallbackQuery) -> None:
    movies_list = get_movies_list(selected_genre, COUNTS_MOVIES)
    movies = generate_message_with_movies_list(movies_list)
    ganre = get_genre(selected_genre, GENRES).lower()
    query.message.reply_text(
        f'Вот {COUNTS_MOVIES} случайных фильмов жанра <b>{ganre}</b>:\n{movies}',
        reply_markup=get_keyboard_select_others_and_select_genre(selected_genre),
        parse_mode=ParseMode.HTML
    )


def main() -> None:
    load_dotenv()

    updater = Updater(os.getenv('TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        CallbackQueryHandler(find_out_genre_of_film, pattern='^выбрать жанр$')
    )
    dispatcher.add_handler(
        CallbackQueryHandler(send_list_of_other_movies, pattern='выбрать_другие')
    )
    dispatcher.add_handler(CallbackQueryHandler(send_movies_list))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
