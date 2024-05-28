from telegram import ParseMode, ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater
)


def get_start_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Заполнить анкету']
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def start_bot(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Я бот! Зачем я создан?!', reply_markup=get_start_keyboard())


def questionnaire_start(update: Update, context: CallbackContext) -> str:
    keyboard = ReplyKeyboardMarkup(
        [
            ['отмена']
        ],
        resize_keyboard=True,
    )
    update.message.reply_text('Введите ваше имя:', reply_markup=keyboard)
    return 'name'


def get_name(update: Update, context: CallbackContext) -> str:
    context.user_data['name'] = update.message.text
    update.message.reply_text('Введите вашу фамилию:')
    return 'surname'


def get_surname(update: Update, context: CallbackContext) -> str:
    context.user_data['surname'] = update.message.text
    update.message.reply_text('Введите ваш возраст:')
    return 'age'


def get_age(update: Update, context: CallbackContext) -> str:
    age = int(update.message.text)
    if age < 0 or age > 99:
        update.message.reply_text('Введите ваш возраст:')
        return 'age'
    context.user_data['age'] = age
    update.message.reply_text('Введите ваш номер телефона:')
    return 'phone_number'


def get_phone_number(update: Update, context: CallbackContext) -> int:
    phone_number = update.message.text
    update.message.reply_text(
        f'<b>Имя:</b> {context.user_data["name"]}\n'
        f'<b>Фамилия:</b> {context.user_data["surname"]}\n'
        f'<b>Возраст:</b> {context.user_data["age"]}\n'
        f'<b>Номер телефона:</b> {phone_number}',
        reply_markup=get_start_keyboard(),
        parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


# def get_phone_number(update: Update, context: CallbackContext) -> int:
#     phone_number = update.message.text
#     update.message.reply_text(
#         f'*Имя:* {context.user_data["name"]}\n'
#         f'*Фамилия:* {context.user_data["surname"]}\n'
#         f'*Возраст:* {context.user_data["age"]}\n'
#         f'*Номер телефона:* {phone_number}',
#         reply_markup=get_start_keyboard(),
#         parse_mode=ParseMode.MARKDOWN_V2
#     )
#     return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Очень жаль, что вы так рано уходите',
        reply_markup=get_start_keyboard()
    )
    return ConversationHandler.END


def main() -> None:
    updater = Updater('TOKEN')
    dispatcher = updater.dispatcher

    questionnaire_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^Заполнить анкету$'), questionnaire_start)],
        states={
            'name': [MessageHandler(Filters.text & ~Filters.regex('^отмена$'), get_name)],
            'surname': [MessageHandler(Filters.text & ~Filters.regex('^отмена$'), get_surname)],
            'age': [MessageHandler(Filters.text & ~Filters.regex('^отмена$'), get_age)],
            'phone_number': [MessageHandler(Filters.text & ~Filters.regex('^отмена$'), get_phone_number)],
        },
        fallbacks=[MessageHandler(Filters.regex('^отмена$'), cancel)]
    )

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(questionnaire_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
