from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler
)
import taskservice

EXPECT_ID = 0

def delete_command_callback(update, context):
    update.message.reply_text("Введите ID задачи которую ты хочешь удалить")
    return EXPECT_ID

def delete_by_id_callback(update, context):
    id = update.message.text
    if(not id.isdigit()):
        update.message.reply_text("Ошибка: вы ввели не ID! Повторите ввод")
        return EXPECT_ID
    task = taskservice.find_task_by_id(int(id))
    if (task == None):
        update.message.reply_text('Ничего не найдено, попробуйте другой ID')
        return EXPECT_ID
    result = taskservice.delete_task(int(id))
    update.message.reply_text(f'Задача удалена: {result}')
    return ConversationHandler.END

def cancel_callback(update, context):
    update.message.reply_text('Удаление задачи по ID прервано')
    return ConversationHandler.END

DELETE_HANDLER = ConversationHandler(
    entry_points= [CommandHandler('delete', delete_command_callback)],
    states={
        EXPECT_ID: [MessageHandler(Filters.text & (~Filters.command), delete_by_id_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)]
)