from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Updater
)


def start_bot(update: Update, context: CallbackContext) -> None:
    buttons = [
        [
            InlineKeyboardButton('купить деньги', callback_data=1),
            InlineKeyboardButton('продать деньги', callback_data=2)
        ],
        [InlineKeyboardButton('настройки', callback_data='settings')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text('Я бот! Зачем я создан?!', reply_markup=keyboard)


def main() -> None:
    updater = Updater('TOKEN')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_bot))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
