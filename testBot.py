import telebot
import datetime
import pytz
import json
import traceback

P_TIMEZONE = pytz.timezone('Europe/Moscow') # для определения времени сообщения
TIMEZONE_COMMON_NAME = 'Moscow'



class User():
    def __init__(self):
        self.faculty = ""
        self.group = ""
        self.year = ""

user = User()

# faculty_answer = ""
# group_answer = ""
# number_of_course_answer = ""
# class_answer = ""


bot = telebot.TeleBot('5095964171:AAH0en9UsoV5YU0uR1mSYoGpUKMQOwshUW8')
@bot.message_handler(commands=['start'])  
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton('Геологоразведочный', callback_data='get-Geologo_Facult'),
        telebot.types.InlineKeyboardButton('Горный', callback_data='get-Economic')  
    )  
    keyboard.add(  
        telebot.types.InlineKeyboardButton('ЭМФ', callback_data='get-ЭМФ'),  
        telebot.types.InlineKeyboardButton('Нефтегазовый', callback_data='get-Neftegaz_Facult')  
    )
    keyboard.add(  
        telebot.types.InlineKeyboardButton('Строительный', callback_data='get-Stroit_Facult'),  
        telebot.types.InlineKeyboardButton('Переработка', callback_data='get-Pererabotka_Facult')  
    )
    keyboard.add(  
        telebot.types.InlineKeyboardButton('Фундаментальные', callback_data='get-Fundamental_Facult'),  
        telebot.types.InlineKeyboardButton('Экономический', callback_data='get-Econom_Facult')  
    )     
    bot.send_message(  
        message.chat.id,  
        'Привет, выбери свой факультет\n' +   
        'Если возникли вопросы - напишите /help.',
        reply_markup=keyboard   
    )

@bot.message_handler(commands=['help'])  
def help_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Сообщение поддержки', url='telegram.me/JohnGolt12')  
    )  
    bot.send_message(  
        message.chat.id,  
        'Если вы не видите вашей базы, напишите нам, чтобы мы добавили данную базу :)'
        ,  
        reply_markup=keyboard  
    )


@bot.callback_query_handler(func=lambda call: True)  
def iq_callback(query):  
    data = query.data  
    if data.startswith('get-'):  
        get_ex_callback(query)
    elif data.startswith('group-'):
        get_group_callback(query)
    elif data.startswith('year-'):
        get_year_callback(query)    
        

def get_ex_callback(query):  
    bot.answer_callback_query(query.id) # убираем состояние загрузки
    send_faculty_result(query.message, query.data[4:])

def send_faculty_result(message, ex_code):
    faculty_answer = ex_code
    user.faculty = faculty_answer
    if faculty_answer == "ЭМФ":
        bot.send_chat_action(message.chat.id, 'typing')
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
            telebot.types.InlineKeyboardButton('АХ', callback_data='group-АХ'),
            telebot.types.InlineKeyboardButton('ГМ', callback_data='group-ГМ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ГТС', callback_data='group-ГТС'),
            telebot.types.InlineKeyboardButton('МНМ', callback_data='group-МНМ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('МО', callback_data='group-МО'),
            telebot.types.InlineKeyboardButton('НТС', callback_data='group-НТС')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ПМК', callback_data='group-ПМК'),
            telebot.types.InlineKeyboardButton('ТОА', callback_data='group-ТОА')  
        )   
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ТОП', callback_data='group-ТОП'),
            telebot.types.InlineKeyboardButton('ТХО', callback_data='group-ТХО')  
        ) 
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ПЭ', callback_data='group-ПЭ'),
            telebot.types.InlineKeyboardButton('ТЭ', callback_data='group-ТЭ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ЭРБ', callback_data='group-ЭРБ'),
            telebot.types.InlineKeyboardButton('ЭРС', callback_data='group-ЭРС')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ЭС', callback_data='group-ЭС'),
        )   
        bot.send_message(  
            message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
            reply_markup=keyboard,   
	    parse_mode='HTML'  
        )

def get_group_callback(query):
    bot.answer_callback_query(query.id)
    send_group_result(query.message, query.data[6:])

def send_group_result(message,ex_code):
    group_answer = ex_code
    user.group = group_answer
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
            telebot.types.InlineKeyboardButton('1', callback_data='year-1'),
            telebot.types.InlineKeyboardButton('2', callback_data='year-2')  
        )
    keyboard.add(  
            telebot.types.InlineKeyboardButton('3', callback_data='year-3'),
            telebot.types.InlineKeyboardButton('4', callback_data='year-4')  
        )
    keyboard.add(  
            telebot.types.InlineKeyboardButton('5', callback_data='year-5'),
        )
    bot.send_message(  
        message.chat.id,'Вы выбрали '+ str(user.faculty) + ' факультет,' + str(user.group) + ' группа.' + '\n' + 'Выбери год обучения',
        reply_markup=keyboard,   
	parse_mode='HTML'  
    )  

def get_year_callback(query):
    bot.answer_callback_query(query.id) # убираем состояние загрузки
    send_year_result(query.message, query.data[5:])

def send_year_result(message, ex_code):
    number_of_course_answer = ex_code
    user.year = number_of_course_answer
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(  
        message.chat.id,'Вы выбрали '+ str(user.faculty) + ' факультет,' + str(user.group) + ' группа, ' + str(user.year) + ' курс' + '\n' + 'Напишите предмет через /Предмет',   
	parse_mode='HTML'  
    ) 

    
bot.polling(none_stop=True)
