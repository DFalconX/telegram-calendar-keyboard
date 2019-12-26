#!/usr/bin/python3

import logging
import telepot
import time
import datetime

from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardRemove
from termcolor import colored, cprint

import telegramcalendar


TOKEN = "1037995722:AAGBO4alsSjOl0cxQYSD9cdyQ2LTTZRpEts"

def logMsg(msg,tipo):
    dt = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    tipo = tipo.upper()
    if tipo == "ERROR":
        tipo = colored(tipo, "red")
    elif tipo == "INFO":
        tipo = colored(tipo, "green")
    elif tipo == "WARNING":
        tipo = colored(tipo, "yellow")

    print(tipo + " ["+dt+"]" +": " + msg)


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
    try:

        # Inicializando Chats Autorizados
        logMsg("Iniciando Bot","Info")
        bot = telepot.Bot(TOKEN)
        #Inicia Hilo escucha del chatbot
        MessageLoop(bot, {'chat': calendar_handler,'callback_query': inline_handler}).run_as_thread()

        #### The main loop ####
        while True:     
            time.sleep(300)

    #### Cleaning up at the end
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
