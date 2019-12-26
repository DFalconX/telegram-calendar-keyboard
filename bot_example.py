#!/usr/bin/python3
import logging
import telepot
import time
import datetime

from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardRemove

import telegramcalendar


TOKEN = ""

def calendar_handler(msg):
    chat_id = telepot.glance(msg)[2]
    bot.sendMessage(chat_id, "Please select a date: ", reply_markup=telegramcalendar.create_calendar())


def inline_handler(msg):
    chat_id = msg['message']['chat']['id']
    selected,date = telegramcalendar.process_calendar_selection(bot, msg)
    if selected:
        bot.sendMessage(chat_id,"You selected %s" % (date.strftime("%d/%m/%Y")), reply_markup=ReplyKeyboardRemove())

if TOKEN == "":
    print("Please write TOKEN into file")
else:
    tbot = telepot.Bot(TOKEN)
    MessageLoop(bot, {'chat': calendar_handler,'callback_query': inline_handler}).run_as_thread()
    while True:     
        time.sleep(300)
