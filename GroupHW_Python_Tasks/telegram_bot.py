from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler
)
from config import TOKEN
from datetime import datetime 
import taskservice

def start_callback(update, context):
    context.bot.send_message(update.effective_chat.id, "Тебя приветствует бот по списку задач")

def info_callback(update, context):
    context.bot.send_message(update.effective_chat.id, "Меня создала компания GB!")

def create_task_callback(update, context):
    context.user_data['operation'] = "Создание новой задачи"
    update.message.reply_text("Введите описание задачи")
    return 'ask_description'

def find_tasks_callback(update, context):
    context.user_data['operation'] = "Поиск задач"
    update.message.reply_text("Введите строку для поиска")
    return 'search_result'

def find_task_by_id_callback(update, context):
    context.user_data['operation'] = "Поиск задачи по ID"
    update.message.reply_text("Введите ID для поиска")
    return 'search_by_id_result'

def search_callback(update, context):
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

def search_by_id_callback(update, context):
    id = update.message.text
    if(not id.isdigit()):
        update.message.reply_text("Ошибка: вы ввели не ID! Повторите ввод")
        return 'search_by_id_result'
    task = taskservice.find_task_by_id(int(id))
    if (task == None):
        update.message.reply_text('Ничего не найдено, попробуйте другой ID')
        return 'search_by_id_result'
    update.message.reply_text(f'''
        ID: {task[0]}\n
        Description: {task[1]}\n
        Date: {task[2]}\n
        Status: {task[3]}'''
    )
    return ConversationHandler.END

def update_callback(update, context):
    context.user_data['operation'] = "Обновление задачи по ID"
    update.message.reply_text("Введите ID задачи которую ты хочешь обновить")
    return 'update_by_id'

def update_by_id_callback(update, context):
    id = update.message.text
    if(not id.isdigit()):
        update.message.reply_text("Ошибка: вы ввели не ID! Повторите ввод")
        return 'update_by_id'
    task = taskservice.find_task_by_id(int(id))
    if (task == None):
        update.message.reply_text('Ничего не найдено, попробуйте другой ID')
        return 'update_by_id'
    context.user_data['task_id'] = task[0]
    update.message.reply_text(f'''
        ID: {task[0]}\n
        Description: {task[1]}\n
        Date: {task[2]}\n
        Status: {task[3]}'''
    )
    update_options = [
        [
            InlineKeyboardButton("Описание", callback_data='description'),
            InlineKeyboardButton("Дата", callback_data='date'),
        ]
    ]
    markup = InlineKeyboardMarkup(update_options)
    update.message.reply_text('Что вы хотите обновить?', reply_markup=markup)
    return 'expect_button_click'

def update_button_click_handler(update, context):
    query = update.callback_query
    query.answer(f'button click {query.data} recieved')
    if query.data == 'description':
        query.edit_message_text(f'Вы выбрали изменить описание')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text='Введите новое описание', reply_markup=ForceReply())
        return 'expect_description'
    if query.data == 'date':
        query.edit_message_text(f'Вы выбрали изменить дату')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text='Введите новую дату', reply_markup=ForceReply())
        return 'expect_date'

def update_description_callback(update, context):
    description = update.message.text
    id = context.user_data['task_id']
    result = taskservice.update_task_description(id, description)
    update.message.reply_text(f'Задача изменена: {result}')
    return ConversationHandler.END

def update_date_callback(update, context):
    date = update.message.text
    id = context.user_data['task_id']
    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        update.message.reply_text("Неверный формат даты. Повторите ввод")
        return 'expect_date'
    result = taskservice.update_task_date(id,date)
    update.message.reply_text(f'Задача изменена: {result}')
    return ConversationHandler.END

def delete_by_id_callback(update, context):
    id = update.message.text
    if(not id.isdigit()):
        update.message.reply_text("Ошибка: вы ввели не ID! Повторите ввод")
        return 'delete_by_id'
    task = taskservice.find_task_by_id(int(id))
    if (task == None):
        update.message.reply_text('Ничего не найдено, попробуйте другой ID')
        return 'delete_by_id'
    result = taskservice.delete_task(int(id))
    update.message.reply_text(f'Задача удалена: {result}')
    return ConversationHandler.END

def delete_callback(update, context):
    context.user_data['operation'] = 'Удаление задачи по ID'
    update.message.reply_text("Введите ID задачи которую ты хочешь удалить")
    return 'delete_by_id'

def description_callback(update, context):
    description = update.message.text
    context.user_data['description'] = description
    update.message.reply_text("Введите дату (YYYY-MM-DD)")
    return 'ask_date'

def date_callback(update, context):
    date = update.message.text
    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        update.message.reply_text("Неверный формат даты. Повторите ввод")
        return 'ask_date'
    description = context.user_data['description']
    result = taskservice.create_task(description, date)
    update.message.reply_text(f'Новая задача сохранена: {result}')
    return ConversationHandler.END

def cancel_callback(update, context):
    operation = context.user_data['operation']
    update.message.reply_text(f'{operation} прервано')
    return ConversationHandler.END

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

handlers = {}
handlers['start_handler'] = CommandHandler('start', start_callback)
handlers['info_handler'] = CommandHandler('info', info_callback)
handlers['create_task_conversation_handler'] = ConversationHandler(
    entry_points=[CommandHandler('create', create_task_callback)],
    states={
        'ask_description': [MessageHandler(Filters.text & (~Filters.command), description_callback)],
        'ask_date': [MessageHandler(Filters.text & (~Filters.command), date_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)]
)
handlers['find_tasks'] = ConversationHandler(
    entry_points=[CommandHandler('find', find_tasks_callback)],
    states={
        'search_result': [MessageHandler(Filters.text & (~Filters.command), search_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)]
)
handlers['find_task_by_id'] = ConversationHandler(
    entry_points=[CommandHandler('find_by_id', find_task_by_id_callback)],
    states={
        'search_by_id_result': [MessageHandler(Filters.text & (~Filters.command), search_by_id_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)]
)
handlers['update'] = ConversationHandler(
    entry_points=[CommandHandler('update', update_callback)],
    states={
        'update_by_id': [MessageHandler(Filters.text & (~Filters.command), update_by_id_callback)],
        'expect_button_click': [CallbackQueryHandler(update_button_click_handler)],
        'expect_description': [MessageHandler(Filters.text & (~Filters.command), update_description_callback)],
        'expect_date': [MessageHandler(Filters.text & (~Filters.command), update_date_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)]
)
handlers['delete'] = ConversationHandler(
    entry_points= [CommandHandler('delete', delete_callback)],
    states={
        'delete_by_id': [MessageHandler(Filters.text & (~Filters.command), delete_by_id_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)]
)

for key, value in handlers.items():
    dispatcher.add_handler(value)
    print(f'Добавлен обработчик {key}')

print('server started')
updater.start_polling()
updater.idle()