#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# Credits: grcanosa https://github.com/grcanosa
#
# Telepot Version: https://github.com/DFalconX/telegram-calendar-keyboard
"""
Base methods for calendar keyboard creation and processing.
"""
import telepot
import datetime
import calendar

from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove


def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(year),str(month),str(day)])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None,month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    row.append(InlineKeyboardButton(text=calendar.month_name[month]+" "+str(year),callback_data=data_ignore))
    keyboard.append(row)
    #Second row - Week Days
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(text=day,callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(text=" ",callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(text=str(day),callback_data=create_callback_data("DAY",year,month,day)))
        keyboard.append(row)
    #Last row - Buttons
    row=[]
    row.append(InlineKeyboardButton(text="<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(text=" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(text=">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))
    keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def process_calendar_selection(bot,update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False,None)
    query = telepot.glance(update, flavor='callback_query')
    query_id = query[0]
    data = query[2]
    chat_id = update['message']['chat']['id']
    message_id = update["message"]["message_id"]
    message_text = update["message"]["text"]
    (action,year,month,day) = separate_callback_data(data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answerCallbackQuery(callback_query_id= query_id)
    elif action == "DAY":
        bot.editMessageText(text=message_text,
            msg_identifier=(chat_id,message_id)
            )
        ret_data = True,datetime.datetime(int(year),int(month),int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.editMessageText(text=message_text,
            msg_identifier=(chat_id,message_id),
            reply_markup=create_calendar(int(pre.year),int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        bot.editMessageText(text=message_text,
            msg_identifier=(chat_id,message_id),
            reply_markup=create_calendar(int(ne.year),int(ne.month)))
    else:
        bot.answerCallbackQuery(callback_query_id= update["id"],text="Something went wrong!")
        # UNKNOWN
    return ret_data
