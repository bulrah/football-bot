from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

TOKEN = os.getenv('TOKEN')

match_database = {
    "Арсенал - Челси": "✅ Анализ матча Арсенал - Челси:\n\nАрсенал в сильной форме, но проблемы в атаке. Челси нестабилен, но может быть опасен в контратаках. Главный фактор — травмированный Салах. Вероятна ничья 1-1.",
    "Ман Сити - Ливерпуль": "🔥 Анализ матча Ман Сити - Ливерпуль:\n\nМан Сити дома силен, но Ливерпуль в этом сезоне неудержим. Ожидается много голов. Возможен счет 2-2.",
}

def start_command(update: Update, context: CallbackContext):
    keyboard = [['Матчи сегодня']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Привет! Я футбольный аналитик. Нажми «Матчи сегодня», чтобы увидеть игры.', reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text

    if user_text == 'Матчи сегодня':
        matches_list = list(match_database.keys())
        if not matches_list:
            update.message.reply_text('На сегодня матчей нет!')
            return
        keyboard = [[match] for match in matches_list]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text('Выберите матч:', reply_markup=reply_markup)
    elif user_text in match_database:
        analysis = match_database[user_text]
        update.message.reply_text(analysis)
    else:
        update.message.reply_text('Пожалуйста, используйте кнопки.')

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
