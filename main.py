#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

text = """Hey there !
If you're looking for today's class backup then you're at right place.
Please follow the guidelines else you'll be BANNED from using Backup Facility.\n
- Gurtej Sahni Classes
www.gurtejsahniclasses.com"""

def start(bot, update):
    custom_keyboard = [['CA FOUNDATION'], 
                   ['CA INTERMEDIATE'],
                   ['CA FINAL']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(text, reply_text=reply_text)


def help(bot, update):
    update.message.reply_text('Help!')


def msg_handler(bot, update):
    msg = update.message.text
    if msg == "CA FOUNDATION":
        custom_keyboard = [['Accounting', 'Economics'], 
                   ['Law', 'Mathematics'], ['Main Menu']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "CA INTERMEDIATE": 
        custom_keyboard = [['Group 1', 'Group 2'],
                   ['Main Menu']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "Group 1": 
        custom_keyboard = [['Accounts'], ['Cost'], ['Tax']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "Group 2": 
        custom_keyboard = [['Advanced Accounting'], ['FM & ECO']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "CA FINAL": 
        custom_keyboard = [['Financial Reporting', 'Strategic Cost Management'],
                   ['Strategic Financial Management'], ['Main Menu']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "Main Menu": 
        custom_keyboard = [['CA FOUNDATION'], 
                   ['CA INTERMEDIATE'],
                   ['CA FINAL']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(msg, reply_text=reply_text)


def error(bot, update):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    try:
        token = sys.argv[1]
    except IndexError:
        token = os.environ.get("TOKEN")
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, msg_handler))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Ready to rock..!")
    updater.idle()


if __name__ == '__main__':
    main()
