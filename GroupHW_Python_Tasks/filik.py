''' A simple conversation bot, that takes user's name and saves it.
- Uses pickle persistence for storing data. You can easily use other ways.
- Uses polling for fetching updates, you can easily use webhooks.
Commands:
/start - replies if alive
/set_name - start a conversation to save name
/get_name - replies with user's name, if saved, else tells user to /set_name
'''

import logging
from telegram.ext.filters import Filters

from telegram.ext.messagehandler import MessageHandler
from config import TOKEN
from telegram import Update
from telegram.ext import (Updater,
                          PicklePersistence,
                          CommandHandler,
                          CallbackQueryHandler,
                          CallbackContext,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply


EXPECT_NAME, EXPECT_BUTTON_CLICK = range(2)

print(EXPECT_BUTTON_CLICK)

def start(update: Update, context: CallbackContext):
    ''' Replies to start command '''
    update.message.reply_text('Hi! I am alive')


def set_name_handler(update: Update, context: CallbackContext):
    ''' Entry point of conversation  this gives  buttons to user'''

    button = [[InlineKeyboardButton("name", callback_data='name')]]
    markup = InlineKeyboardMarkup(button)

    # you can add more buttons here

    #  learn more about inline keyboard
    # https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example

    update.message.reply_text('Name button', reply_markup=markup)

    return EXPECT_BUTTON_CLICK


def button_click_handler(update: Update, context: CallbackContext):
    ''' This gets executed on button click '''
    query = update.callback_query
    # shows a small notification inside chat
    query.answer(f'button click {query.data} recieved')

    if query.data == 'name':
        query.edit_message_text(f'You clicked on "name"')
        # asks for name, and prompts user to reply to it
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send your name', reply_markup=ForceReply())
        # learn more about forced reply
        # https://python-telegram-bot.readthedocs.io/en/stable/telegram.forcereply.html
        return EXPECT_NAME


def name_input_by_user(update: Update, context: CallbackContext):
    ''' The user's reply to the name prompt comes here  '''
    name = update.message.text

    # saves the name
    context.user_data['name'] = name
    update.message.reply_text(f'Your name is saved as {name[:100]}')

    # ends this particular conversation flow
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Name Conversation cancelled by user. Bye. Send /set_name to start again')
    return ConversationHandler.END


def get_name(update: Update, context: CallbackContext):
    ''' Handle the get_name command. Replies the name of user if found. '''
    value = context.user_data.get(
        'name', 'Not found. Set your name using /set_name command')
    update.message.reply_text(value)


if __name__ == "__main__":

    #  learn more about persistence
    # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent
    # pickle persistence
    # https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.picklepersistence.html
    # example
    # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/persistentconversationbot.py

    #  if you are deploying on cloud, connecting to a database may help
    #  because platforms like heroku deletes all extra files

    pp = PicklePersistence(filename='mybot')
    updater = Updater(token=TOKEN, persistence=pp)

    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    _handlers = {}

    _handlers['start_handler'] = CommandHandler('start', start)

    # learn more about conversation handler

    # official docs
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.conversationhandler.html

    # official example
    # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py

    _handlers['name_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('set_name', set_name_handler)],
        states={
            EXPECT_NAME: [MessageHandler(Filters.text, name_input_by_user)],
            EXPECT_BUTTON_CLICK: [CallbackQueryHandler(button_click_handler)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    _handlers['get_name'] = CommandHandler('get_name', get_name)

    for name, _handler in _handlers.items():
        print(f'Adding handler {name}')
        dispatcher.add_handler(_handler)

    updater.start_polling()

    updater.idle()