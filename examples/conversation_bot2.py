from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater
)


def start_bot(update: Update, context: CallbackContext) -> None:
    keyboard = ReplyKeyboardMarkup(
        [
            ['Заполнить анкету']
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_text('Я бот! Зачем я создан?!', reply_markup=keyboard)


def questionnaire_start(update: Update, context: CallbackContext) -> str:
    update.message.reply_text('Введите ваше имя:')
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
    context.user_data['age'] = update.message.text
    update.message.reply_text('Введите ваш номер телефона:')
    return 'phone_number'


def get_phone_number(update: Update, context: CallbackContext) -> int:
    phone_number = update.message.text
    update.message.reply_text(
        f'Имя: {context.user_data["name"]}\n'
        f'Фамилия: {context.user_data["surname"]}\n'
        f'Возраст: {context.user_data["age"]}\n'
        f'Номер телефона: {phone_number}'
    )
    return ConversationHandler.END


def main() -> None:
    updater = Updater('TOKEN')
    dispatcher = updater.dispatcher

    questionnaire_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^Заполнить анкету$'), questionnaire_start)],
        states={
            'name': [MessageHandler(Filters.text, get_name)],
            'surname': [MessageHandler(Filters.text, get_surname)],
            'age': [MessageHandler(Filters.text, get_age)],
            'phone_number': [MessageHandler(Filters.text, get_phone_number)],
        },
        fallbacks=[]
    )

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(questionnaire_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
