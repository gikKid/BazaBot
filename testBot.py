import telebot
import datetime
import pytz
import json
import traceback

P_TIMEZONE = pytz.timezone('Europe/Moscow') # для определения времени сообщения
TIMEZONE_COMMON_NAME = 'Moscow'

class_answer = ""
number_of_course_answer = ""


bot = telebot.TeleBot('5095964171:AAH0en9UsoV5YU0uR1mSYoGpUKMQOwshUW8')
@bot.message_handler(commands=['start'])  
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton('Chemistry', callback_data='get-Chemistry'),
        telebot.types.InlineKeyboardButton('Economic', callback_data='get-Economic')  
    )  
    keyboard.add(  
        telebot.types.InlineKeyboardButton('FOE', callback_data='get-FOE'),  
        telebot.types.InlineKeyboardButton('Microelectronic', callback_data='get-Microelectronic')  
    )   
    bot.send_message(  
        message.chat.id,  
        'Hello,choose a class\n' +   
        'To get help write /help.',
        reply_markup=keyboard   
    )

@bot.message_handler(commands=['help'])  
def help_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Message the developer', url='telegram.me/JohnGolt12')  
    )  
    bot.send_message(  
        message.chat.id,  
        '1)If u have some payment problems - press button below to write supporter about it\n' +
        '2)If u didnt see specific class base - write to email @nesterenkoegorbussines@gmail.com and we will fix it fast\n'
        ,  
        reply_markup=keyboard  
    )


@bot.callback_query_handler(func=lambda call: True)  
def iq_callback(query):  
    data = query.data  
    if data.startswith('get-'):  
        get_ex_callback(query)

def get_ex_callback(query):  
    bot.answer_callback_query(query.id) # убираем состояние загрузки
    send_class_result(query.message, query.data[4:])

def send_class_result(message, ex_code):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(  
        message.chat.id, str(ex_code),  
        #reply_markup=get_update_keyboard(ex_code),  
	parse_mode='HTML'  
    )

# def get_update_keyboard(ex):  
#     keyboard = telebot.types.InlineKeyboardMarkup()  
#     keyboard.row(  
#         telebot.types.InlineKeyboardButton('1'),  
# 	    telebot.types.InlineKeyboardButton('2'),
#         telebot.types.InlineKeyboardButton('3'),
#         telebot.types.InlineKeyboardButton('4')
#     )  
#     return keyboard

# @bot.message_handler(commands=['1'])
# def first_command(message):
#      number_of_course_answer = "1"
#      bot.send_message(message.chat.id, "We took your answers: " + str(class_answer) + str(number_of_course_answer) + "\nwrite /pay to pay 0.5$ and start learning")       
    




    
bot.polling(none_stop=True)
