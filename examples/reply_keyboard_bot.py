from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater
)


def start_bot(update: Update, context: CallbackContext) -> None:
    keyboard = ReplyKeyboardMarkup(
        [
            ['/start', '/help'],
            ['купить деньги']
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_text('Я бот! Зачем я создан?!', reply_markup=keyboard)


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    updater = Updater('TOKEN')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
