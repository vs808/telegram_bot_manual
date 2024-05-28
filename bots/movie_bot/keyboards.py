from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_with_genres(genres: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = []
    index_of_button = 0
    for genre in genres:
        if index_of_button % 2 == 0:
            keyboard.append(
                [InlineKeyboardButton(genre, callback_data=genres[genre])]
            )
        else:
            keyboard[index_of_button // 2].append(
                InlineKeyboardButton(genre, callback_data=genres[genre])
            )
        index_of_button += 1
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
