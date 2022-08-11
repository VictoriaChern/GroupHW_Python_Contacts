from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler
)
from datetime import datetime
import taskservice

EXPECT_ID, EXPECT_BUTTON_CLICK, EXPECT_DESCRIPTION, EXPECT_DATE = range(4)

def update_command_callback(update, context):
    update.message.reply_text("Введите ID задачи которую ты хочешь обновить")
    return EXPECT_ID

def update_menu_callback(update, context):
    id = update.message.text
    if(not id.isdigit()):
        update.message.reply_text("Ошибка: вы ввели не ID! Повторите ввод")
        return EXPECT_ID
    task = taskservice.find_task_by_id(int(id))
    if (task == None):
        update.message.reply_text('Ничего не найдено, попробуйте другой ID')
        return EXPECT_ID
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
    return EXPECT_BUTTON_CLICK

def update_button_click_callback(update, context):
    query = update.callback_query
    query.answer(f'button click {query.data} recieved')
    if query.data == 'description':
        query.edit_message_text(f'Вы выбрали изменить описание')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text='Введите новое описание', reply_markup=ForceReply())
        return EXPECT_DESCRIPTION
    if query.data == 'date':
        query.edit_message_text(f'Вы выбрали изменить дату')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text='Введите новую дату', reply_markup=ForceReply())
        return EXPECT_DATE

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

def cancel_callback(update, context):
    update.message.reply_text('Обновление задачи по ID прервано')
    return ConversationHandler.END

UPDATE_HANDLER = ConversationHandler(
    entry_points=[CommandHandler('update', update_command_callback)],
    states={
        EXPECT_ID: [MessageHandler(Filters.text & (~Filters.command), update_menu_callback)],
        EXPECT_BUTTON_CLICK: [CallbackQueryHandler(update_button_click_callback)],
        EXPECT_DESCRIPTION: [MessageHandler(Filters.text & (~Filters.command), update_description_callback)],
        EXPECT_DATE: [MessageHandler(Filters.text & (~Filters.command), update_date_callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)]
)