from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Updater
)


def start_bot(update: Update, context: CallbackContext) -> None:
    buttons = [
        [
            InlineKeyboardButton('купить деньги', callback_data='купить деньги'),
            InlineKeyboardButton('продать деньги', callback_data='продать деньги')
        ],
        [InlineKeyboardButton('настройки', callback_data='settings')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text('Я бот! Зачем я создан?!', reply_markup=keyboard)


def buy_money(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.reply_text('Вы купили 100 денег')


def sell_money(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.reply_text('Вы продали 100 денег')


def settings(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.reply_text('Настройки настроены')


def main() -> None:
    updater = Updater('TOKEN')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(CallbackQueryHandler(buy_money, pattern='^купить деньги$'))
    dispatcher.add_handler(CallbackQueryHandler(sell_money, pattern='^продать деньги$'))
    dispatcher.add_handler(CallbackQueryHandler(settings, pattern='^settings$'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
