import telebot
from telebot import types
from os import write
import docx
import json
import io
import pytz
import config

P_TIMEZONE = pytz.timezone('Europe/Moscow') # для определения времени сообщения
TIMEZONE_COMMON_NAME = 'Moscow'


class User():
    def __init__(self):
        self.faculty = ""
        self.group = ""
        self.year = ""
        self.subject = ""
        self.semester = ""
        self.document = ""

user = User()

bot = telebot.TeleBot(config.apikey)
@bot.message_handler(commands=['start'])  
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton('Геологоразведочный', callback_data='get-Геологоразведочный'),
        telebot.types.InlineKeyboardButton('Горный', callback_data='get-Горный')  
    )  
    keyboard.add(  
        telebot.types.InlineKeyboardButton('ЭМФ', callback_data='get-ЭМФ'),  
        telebot.types.InlineKeyboardButton('Нефтегазовый', callback_data='get-Нефтегазовый')  
    )
    keyboard.add(  
        telebot.types.InlineKeyboardButton('Строительный', callback_data='get-Строительный'),  
        telebot.types.InlineKeyboardButton('Переработка', callback_data='get-Переработка')  
    )
    keyboard.add(  
        telebot.types.InlineKeyboardButton('Фундаментальные', callback_data='get-Фундаментальные'),  
        telebot.types.InlineKeyboardButton('Экономический', callback_data='get-Экономический')  
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
    elif data.startswith('semester-'):
        get_semester_callback(query)
    elif data.startswith('document-'):
        get_document_callback(query)   
        
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'TestDocuments/' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Документ получен...")
    except Exception as e:
        bot.reply_to(message, e)


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
    elif faculty_answer == "Геологоразведочный":
        bot.send_chat_action(message.chat.id, 'typing')
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ГНГ', callback_data='group-ГНГ'),
            telebot.types.InlineKeyboardButton('МГП', callback_data='group-МГП')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('РГИ', callback_data='group-РГИ'),
            telebot.types.InlineKeyboardButton('РФ', callback_data='group-РФ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('РФС', callback_data='group-РФС'),
            telebot.types.InlineKeyboardButton('НТС', callback_data='group-НТС')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('РМ', callback_data='group-РМ'),
            telebot.types.InlineKeyboardButton('РГГ', callback_data='group-РГГ')  
        )  
        bot.send_message(  
            message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
            reply_markup=keyboard,   
	    parse_mode='HTML'  
        )
    elif faculty_answer == "Горный":
        bot.send_chat_action(message.chat.id, 'typing')
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
            telebot.types.InlineKeyboardButton('БТС', callback_data='group-БТС'),
            telebot.types.InlineKeyboardButton('ВД', callback_data='group-ВД')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ИЗС', callback_data='group-ИЗС'),
            telebot.types.InlineKeyboardButton('ТО', callback_data='group-ТО')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ТПП', callback_data='group-ТПП'),
            telebot.types.InlineKeyboardButton('ТПР', callback_data='group-ТПР')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('БТБ', callback_data='group-БТБ'),
            telebot.types.InlineKeyboardButton('ИЗБ', callback_data='group-ИЗБ')  
        )   
        bot.send_message(  
            message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
            reply_markup=keyboard,   
	    parse_mode='HTML'  
        )
    elif faculty_answer == "Нефтегазовый":
        bot.send_chat_action(message.chat.id, 'typing')
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
            telebot.types.InlineKeyboardButton('НГС', callback_data='group-НГС'),
            telebot.types.InlineKeyboardButton('РТ', callback_data='group-РТ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ГРП', callback_data='group-ГРП'),
            telebot.types.InlineKeyboardButton('ДГ', callback_data='group-НБ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('НБШ', callback_data='group-НБШ'),
            telebot.types.InlineKeyboardButton('НГШ', callback_data='group-НГШ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('НД', callback_data='group-НД'),
            telebot.types.InlineKeyboardButton('СТ', callback_data='group-СТ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ТНГ', callback_data='group-ТНГ'),
            telebot.types.InlineKeyboardButton('ЭХТ', callback_data='group-ЭХТ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('КРС', callback_data='group-КРС'),
            telebot.types.InlineKeyboardButton('НБС', callback_data='group-НБС')  
        )   
        bot.send_message(  
            message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
            reply_markup=keyboard,   
	    parse_mode='HTML'  
        )
    elif faculty_answer == "Строительный":
        bot.send_chat_action(message.chat.id, 'typing')
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ГГ', callback_data='group-ГГ'),
            telebot.types.InlineKeyboardButton('ГС', callback_data='group-ГС')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('АГС', callback_data='group-АГС'),
            telebot.types.InlineKeyboardButton('ИГ', callback_data='group-ИГ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('СПС', callback_data='group-СПС'),
            telebot.types.InlineKeyboardButton('ГК', callback_data='group-ГК')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ПГС', callback_data='group-ПГС'),
        )  
        bot.send_message(  
            message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
            reply_markup=keyboard,   
	    parse_mode='HTML'  
        )
    elif faculty_answer == "Переработка":
        bot.send_chat_action(message.chat.id, 'typing')
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ОП', callback_data='group-ОП'),
            telebot.types.InlineKeyboardButton('АПГ', callback_data='group-АПГ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('АПМ', callback_data='group-АПМ'),
            telebot.types.InlineKeyboardButton('АПН', callback_data='group-АПН')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('МЦ', callback_data='group-МЦ'),
            telebot.types.InlineKeyboardButton('ОНГ', callback_data='group-ОНГ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ТХ', callback_data='group-ТХ'),
            telebot.types.InlineKeyboardButton('ТХН', callback_data='group-ТХН')
        )  
        bot.send_message(  
            message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
            reply_markup=keyboard,   
	    parse_mode='HTML'  
        )
    elif faculty_answer == "Фундаментальные":
        bot.send_chat_action(message.chat.id, 'typing')
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ИАС', callback_data='group-ИАС'),
            telebot.types.InlineKeyboardButton('ИСТ', callback_data='group-ИСТ')  
        )
        bot.send_message(  
            message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
            reply_markup=keyboard,   
	    parse_mode='HTML'  
        )
    elif faculty_answer == "Экономический":
        bot.send_chat_action(message.chat.id, 'typing')
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
            telebot.types.InlineKeyboardButton('ИТУ', callback_data='group-ИТУ'),
            telebot.types.InlineKeyboardButton('МП', callback_data='group-МП')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('САМ', callback_data='group-САМ'),
            telebot.types.InlineKeyboardButton('ЭГ', callback_data='group-ЭГ')  
        )
        keyboard.add(  
            telebot.types.InlineKeyboardButton('БА', callback_data='group-БА'),
            telebot.types.InlineKeyboardButton('МТ', callback_data='group-МТ')  
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
        message.chat.id,'Вы выбрали '+ str(user.faculty) + ' факультет,' + str(user.group) + ' группа.' + '\n' + 'Выберите год обучения',
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
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton('1', callback_data='semester-1'),
        telebot.types.InlineKeyboardButton('2', callback_data='semester-2')  
    )
    bot.send_message(  
        message.chat.id,'Вы выбрали '+ str(user.faculty) + ' факультет,' + str(user.group) + ' группа, ' + str(user.year) + ' курс' + '\n' + 'Выберите семестр"',
    reply_markup=keyboard,   
	parse_mode='HTML'  
    ) 

def get_semester_callback(query): 
    bot.answer_callback_query(query.id)
    send_semester_result(query.message, query.data[9:])


def send_semester_result(message, ex_code):
    user.semester = ex_code
    with open('shablonBaza.png','rb') as photo_object:
        photo = photo_object
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_photo(message.chat.id,photo)
        keyboard = telebot.types.InlineKeyboardMarkup()  
        keyboard.add(  
        telebot.types.InlineKeyboardButton('table', callback_data='document-table'),
        )
        bot.send_message(  
            message.chat.id,'Вы выбрали ' + str(user.semester) + " семестр\n" + 
            "Выберите базу, если интересующуюся база отсутствует, тогда вставьте свою\n" + 
            "ОБЯЗАТЕЛЬНО ПРОВЕРЬТЕ ЧТОБЫ ВАША БАЗА СООТВЕТСТВОВАЛА ШАБЛОНУ ФОТОГРАФИИ СВЕРХУ !",
        reply_markup=keyboard,   
	    parse_mode='HTML'  
        )
        

def get_document_callback(query):
    bot.answer_callback_query(query.id)
    send_document_result(query.message, query.data[9:])

def send_document_result(message,ex_code):
    user.document = ex_code
    with open("table.json") as document_obj:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        markup.add(btn1, btn2,btn3,btn4)
        data = json.load(document_obj)
        for number in data:
            bot.send_message(message.chat.id,
             number['Вопрос'] + "\n" + number['Ответ'],
            reply_markup=markup,   
	        parse_mode='HTML'  
            )



bot.polling(none_stop=True)
