from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constants import NUMBER_OF_BUTTONS_IN_ROW


def get_keyboard_with_genres(genres: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    for genre in genres:
        row.append(InlineKeyboardButton(genre, callback_data=genres[genre]))
        if len(row) == NUMBER_OF_BUTTONS_IN_ROW:
            keyboard.append(row)
            row = []
    return InlineKeyboardMarkup(keyboard)


def get_keyboard_select_genre() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([_get_button_select_genre()])


def get_keyboard_select_others_and_select_genre(genre: str) -> InlineKeyboardMarkup:
    button = [
        [
            InlineKeyboardButton(
                'выбрать другие фильмы',
                callback_data=f'выбрать_другие {genre}'
            )
        ],
        _get_button_select_genre()
    ]
    return InlineKeyboardMarkup(button)


def _get_button_select_genre() -> InlineKeyboardButton:
    return [InlineKeyboardButton('выбрать жанр', callback_data='выбрать жанр')]
