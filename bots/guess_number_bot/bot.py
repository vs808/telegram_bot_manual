import os
from random import randint

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater
)


BEGINNING_OF_RANGE = 0
END_OF_RANGE = 100


def get_keyboard_start_game() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            ['начать игру']
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_keyboard_end_game() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            ['выйти из игры']
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def start_bot(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f'Привет, {update.message.chat.first_name}! '
        'Нажми "начать игру", чтобы сыграть со мной в угадай число',
        reply_markup=get_keyboard_start_game()
    )


def start_game(update: Update, context: CallbackContext) -> str:
    context.user_data['number'] = randint(BEGINNING_OF_RANGE, END_OF_RANGE)
    context.user_data['count'] = 1
    update.message.reply_text(
        f'Я загал число от {BEGINNING_OF_RANGE} до {END_OF_RANGE}. '
        'Попробуй его угадать. Твой вариант:',
        reply_markup=get_keyboard_end_game()
    )
    return 'game'


def game(update: Update, context: CallbackContext) -> str | int:
    user_number = int(update.message.text)
    if user_number < BEGINNING_OF_RANGE or user_number > END_OF_RANGE:
        update.message.reply_text(
            'Ты вышел за границы диапазона, попробуй еще раз:'
        )
        return 'game'
    bot_number = context.user_data['number']
    if bot_number == user_number:
        update.message.reply_text(
            f'Молодец! Ты угадал число c {context.user_data["count"]} попытки!',
            reply_markup=get_keyboard_start_game()
        )
        return ConversationHandler.END
    if bot_number > user_number:
        update.message.reply_text('Мое число больше, попробуй еще раз:')
    elif bot_number < user_number:
        update.message.reply_text('Мое число меньше, попробуй еще раз:')
    context.user_data['count'] += 1
    return 'game'


def end_game(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Очень жаль, что мы не доиграли(',
        reply_markup=get_keyboard_start_game()
    )
    return ConversationHandler.END


def invalid_input(update: Update, context: CallbackContext) -> str:
    update.message.reply_text('Так не пойдет. Введи число:')
    return 'game'


def get_game_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^начать игру$'), start_game)],
        states={'game': [MessageHandler(Filters.regex('^[+-]?\d+$'), game)]},
        fallbacks=[
            MessageHandler(Filters.regex('^выйти из игры$'), end_game),
            MessageHandler(Filters.text, invalid_input)
        ],
        allow_reentry=True
    )


def main() -> None:
    load_dotenv()

    updater = Updater(os.getenv('TOKEN'))
    dispatcher = updater.dispatcher

    game_handler = get_game_handler()

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(game_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
