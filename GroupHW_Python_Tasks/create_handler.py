from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler
)
from datetime import datetime 
import taskservice

EXPECT_DESCRIPTION, EXPECT_DATE = range(2)

def create_command_callback(update, context):
    update.message.reply_text("Введите описание задачи")
    return EXPECT_DESCRIPTION

def description_callback(update, context):
    description = update.message.text
    context.user_data['description'] = description
    update.message.reply_text("Введите дату (YYYY-MM-DD)")
    return EXPECT_DATE

def date_callback(update, context):
    date = update.message.text
    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        update.message.reply_text("Неверный формат даты. Повторите ввод")
        return EXPECT_DATE
    description = context.user_data['description']
    result = taskservice.create_task(description, date)
    update.message.reply_text(f'Новая задача сохранена: {result}')
    return ConversationHandler.END

def cancel_callback(update, context):
    update.message.reply_text('Создание новой задачи прервано')
    return ConversationHandler.END

CREATE_TASK_HANDLER = ConversationHandler(
    entry_points=[CommandHandler('create', create_command_callback)],
    states={
        EXPECT_DESCRIPTION: [MessageHandler(Filters.text & (~Filters.command), description_callback)],
        EXPECT_DATE: [MessageHandler(Filters.text & (~Filters.command), date_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)]
)