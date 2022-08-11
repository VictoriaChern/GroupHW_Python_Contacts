from telegram import Bot
from telegram.ext import Updater, CommandHandler
from config import TOKEN
from create_handler import CREATE_TASK_HANDLER
from search_handler import FIND_TASKS_HANDLER, FIND_BY_ID_HANDLER
from update_handler import UPDATE_HANDLER
from delete_handler import DELETE_HANDLER

def start_callback(update, context):
    context.bot.send_message(update.effective_chat.id, "Тебя приветствует бот по списку задач")

def info_callback(update, context):
    context.bot.send_message(update.effective_chat.id, "Меня создала компания GB!")

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

handlers = {
    'start_handler'   : CommandHandler('start', start_callback),
    'info_handler'    : CommandHandler('info', info_callback),
    'create_handler'  : CREATE_TASK_HANDLER,
    'find_tasks'      : FIND_TASKS_HANDLER,
    'find_task_by_id' : FIND_BY_ID_HANDLER,
    'update'          : UPDATE_HANDLER,
    'delete'          : DELETE_HANDLER
}

for key, value in handlers.items():
    dispatcher.add_handler(value)
    print(f'Добавлен обработчик {key}')

print('Бот запущен!')
updater.start_polling()
updater.idle()