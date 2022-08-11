from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler
)
import taskservice

# Поиск задач по всем полям

EXPECT_SEARCH_QUERY = 0

def find_command_callback(update, context):
    update.message.reply_text("Введите строку для поиска")
    return EXPECT_SEARCH_QUERY

def find_tasks_callback(update, context):
    search = update.message.text
    tasks = taskservice.find_tasks(search)
    if (tasks == None or len(tasks) == 0):
        update.message.reply_text('Ничего не найдено, попробуйте еще раз')
        return 'search_result'
    for task in tasks:
        update.message.reply_text(f'''
            ID: {task[0]}\n
            Description: {task[1]}\n
            Date: {task[2]}\n
            Status: {task[3]}'''
        )
    return ConversationHandler.END

def cancel_find_callback(update, context):
    update.message.reply_text('Поиск задач прерван')
    return ConversationHandler.END

FIND_TASKS_HANDLER = ConversationHandler(
    entry_points=[CommandHandler('find', find_command_callback)],
    states={
        EXPECT_SEARCH_QUERY : [MessageHandler(Filters.text & (~Filters.command), find_tasks_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_find_callback)]
)

# Поиск задач по ID

EXPECT_ID = 0

def find_by_id_command_callback(update, context):
    update.message.reply_text("Введите ID для поиска")
    return EXPECT_ID

def find_task_by_id_callback(update, context):
    id = update.message.text
    if(not id.isdigit()):
        update.message.reply_text("Ошибка: вы ввели не ID! Повторите ввод")
        return EXPECT_ID
    task = taskservice.find_task_by_id(int(id))
    if (task == None):
        update.message.reply_text('Ничего не найдено, попробуйте другой ID')
        return EXPECT_ID
    update.message.reply_text(f'''
        ID: {task[0]}\n
        Description: {task[1]}\n
        Date: {task[2]}\n
        Status: {task[3]}'''
    )
    return ConversationHandler.END

def cancel_find_by_id_callback(update, context):
    update.message.reply_text('Поиск задачи по ID прерван')
    return ConversationHandler.END

FIND_BY_ID_HANDLER = ConversationHandler(
    entry_points=[CommandHandler('find_by_id', find_by_id_command_callback)],
    states={
        EXPECT_ID: [MessageHandler(Filters.text & (~Filters.command), find_task_by_id_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_find_by_id_callback)]
)