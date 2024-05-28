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
            ['купить деньги'],
            ['продать деньги']
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_text('Я бот! Зачем я создан?!', reply_markup=keyboard)


def buy_money(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Вы купили 100 денег')


def sell_money(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Вы продали 100 денег')


def keep_quiet_with_smart_look(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Хммм...')


def main() -> None:
    updater = Updater('TOKEN')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(MessageHandler(Filters.regex('^купить деньги$'), buy_money))
    dispatcher.add_handler(MessageHandler(Filters.regex('^продать деньги$'), sell_money))
    dispatcher.add_handler(MessageHandler(Filters.text, keep_quiet_with_smart_look))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
