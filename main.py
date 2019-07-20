#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from telegram import KeyboardButton, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import csv
import firebase_admin
import google.cloud
from google.cloud import firestore
from firebase_admin import credentials, firestore
from mwt import MWT
import datetime

import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()

# experiments

doc_ref = store.collection(u'users').limit(2)

try:
    docs = doc_ref.get()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'Missing data')

file_path = "CSV_FILE_PATH"
collection_name = "COLLECTION_TO_ADD_TO"


def batch_data(iterable, n=1):
    lo = len(iterable)
    for ndx in range(0, lo, n):
        yield iterable[ndx:min(ndx + n, lo)]


data = []
headers = []
with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            for header in row:
                headers.append(header)
            line_count += 1
        else:
            obj = {}
            for idx, item in enumerate(row):
                obj[headers[idx]] = item
            data.append(obj)
            line_count += 1

for batched_data in batch_data(data, 499):
    batch = store.batch()
    for data_item in batched_data:
        doc_ref = store.collection(collection_name).document()
        batch.set(doc_ref, data_item)
    batch.commit()

# end of experiments

text = """Hey there !
If you're looking for today's class backup then you're at right place.
Please follow the guidelines else you'll be BANNED from using Backup Facility.\n
- Gurtej Sahni Classes
www.gurtejsahniclasses.com"""


def start(bot, update):
    update.message.reply_text(text)
    user_id = update.message.from_user.id
    status = False
    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row[f'user_data'] == user_data:
                if row[f'status'] == True:
                    status = True
    # check if the user_id exists in database
    # if it doesn't exist, ask phone number
    if status is False:
        contact_keyboard = KeyboardButton('Share contact', request_contact=True)
        custom_keyboard = [[contact_keyboard]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text(
            "Would you mind sharing your contact?",
            reply_markup=reply_markup)
    else:
        update.message.reply_text(text="You are already registered.")
        today = datetime.date.today()
        joining_date = datetime.date(year, month, day)
        diff = joining_date - today
        days = diff.days
        formatted_message = ""
        update.message.reply_text(formatted_message, parse_mode=ParseMode.MARKDOWN)


@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def add_course(bot, update):
    if update.message.from_user.id in get_admin_ids(bot, ):
        # do something
        pass


def help(bot, update):
    update.message.reply_text('Help!')


def contact_handler(bot, update, chat_data):
    # search in csv file to check if the phone number given is registered
    number = update.message.contact
    user_id = update.message.from_user.id
    user_data = chat_data[user_id].split(";")
    course = user_data[0]
    joining_date = user_data[1]
    filename = "database.csv"
    fields = ['user_id', 'phone', 'course', 'joining_date', 'status']
    rows = [[user_id, number, course, joining_date, status]]
    with open(filename, 'w') as csvfile:
        cw = csv.writer(csvfile)
        cw.writerow(fields)
        cw.writerows(rows)
    custom_keyboard = [['CA FOUNDATION'], ['CA INTERMEDIATE'], ['CA FINAL']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(text, reply_text=reply_markup)


def msg_handler(bot, update):
    msg = update.message.text
    if msg in []:
        doc_ref = store.collection(u'test')
        doc_ref.add({u'name': u'test', u'added': u'just now'})
        update.message.reply_text("You have successfully added your course.")
    if msg == "CA FOUNDATION":
        custom_keyboard = [['Accounting', 'Economics'], ['Law', 'Mathematics'], ['Main Menu']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "CA INTERMEDIATE":
        custom_keyboard = [['Group 1', 'Group 2'], ['Main Menu']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "Group 1":
        custom_keyboard = [['Accounts'], ['Cost'], ['Tax']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "Group 2":
        custom_keyboard = [['Advanced Accounting'], ['FM & ECO']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "CA FINAL":
        custom_keyboard = [['Financial Reporting', 'Strategic Cost Management'], ['Strategic Financial Management'], ['Main Menu']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    elif msg == "Main Menu":
        custom_keyboard = [['CA FOUNDATION'], ['CA INTERMEDIATE'], ['CA FINAL']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(msg, reply_text=reply_markup)


class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year


def count_leap(day):
    years = day.year
    if (day.month <= 2):
        years -= 1
    return int(years / 4 - years / 100 + years / 400)


def diff(join, today):
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    start = join.year * 365 + join.day
    for i in range(0, join.month - 1):
        start += month_days[i]
    start += count_leap(join)
    end = today.year * 365 + today.day
    for i in range(0, today.month - 1):
        end += month_days[i]
    end += count_leap(today)
    return (end - start)


# join = Date(13, 12, 2018)
# today = Date(25, 2, 2019)

# print(diff(join, today))


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
    dp.add_handler(MessageHandler(Filters.contact, contact_handler, pass_chat_data=True))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Ready to rock..!")
    updater.idle()


if __name__ == '__main__':
    main()
