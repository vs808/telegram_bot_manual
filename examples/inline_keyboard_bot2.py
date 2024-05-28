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


def reply_when_click_on_inline_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Вы выбрали: {query.data}')


def main() -> None:
    updater = Updater('TOKEN')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(CallbackQueryHandler(reply_when_click_on_inline_button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
