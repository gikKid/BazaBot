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
        self.id = ""
        self.faculty = ""
        self.group = ""
        self.year = ""
        self.semester = ""
        self.document = ""
        self.right_answer = ""
        self.index = 0
        self.data = [{}]
        self.file_Open = False
        self.username = ""

users = []

mining_facults = ["Геологоразведочный","Горный","ЭМФ","Нефтегазовый","Строительный","Переработка","Фундаментальные","Экономический"]
emf_groups = ["AX","ГМ","ГТС","МНМ","МО","НТС","ПМК","ТОА","ТОП","ТХО","ПЭ","ТЭ","ЭРБ","ЭРС","ЭС"]
array_years = ["1","2","3","4"]
array_semesters = ["1","2"]
array_bazs = ['table']
count_answers = ["1","2","3","4"]


bot = telebot.TeleBot(config.apikey)
@bot.message_handler(commands=['start'])
def start_command(message):
    current_users_id = []
    user = User()
    user.id = message.from_user.id
    for user in users:
        current_users_id.append(user.id)
    if user.id not in current_users_id:
        users.append(user)
        print(users)
    print(current_users_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for faculty in mining_facults:
        btn = types.KeyboardButton(faculty)
        markup.add(btn)    
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Выбери свой факультет".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['help'])  
def help_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Сообщение поддержки', url='telegram.me/JohnGolt12')  
    )  
    bot.send_message(  
        message.chat.id,  
        'Если вы не видите вашей базы, или не можете добавить свою - напишите нам, чтобы мы исправили данную ситуацию :)'
        ,  
        reply_markup=keyboard  
    )

        
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


def get_groups(message):
    for item in users:
        if item.id == message.from_user.id:
                if item.faculty == "ЭМФ":
                    print("ЭМФ")
                    bot.send_chat_action(message.chat.id, 'typing')
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for group in emf_groups:
                        btn = types.KeyboardButton(group)
                        markup.add(btn)
                    bot.send_message(message.chat.id, text="Факультет выбран, выберите свою группу".format(message.from_user), reply_markup=markup)
                #     keyboard = telebot.types.InlineKeyboardMarkup()  
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('АХ', callback_data='group-АХ'),
                #         telebot.types.InlineKeyboardButton('ГМ', callback_data='group-ГМ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ГТС', callback_data='group-ГТС'),
                #         telebot.types.InlineKeyboardButton('МНМ', callback_data='group-МНМ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('МО', callback_data='group-МО'),
                #         telebot.types.InlineKeyboardButton('НТС', callback_data='group-НТС')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ПМК', callback_data='group-ПМК'),
                #         telebot.types.InlineKeyboardButton('ТОА', callback_data='group-ТОА')  
                #     )   
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ТОП', callback_data='group-ТОП'),
                #         telebot.types.InlineKeyboardButton('ТХО', callback_data='group-ТХО')  
                #     ) 
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ПЭ', callback_data='group-ПЭ'),
                #         telebot.types.InlineKeyboardButton('ТЭ', callback_data='group-ТЭ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ЭРБ', callback_data='group-ЭРБ'),
                #         telebot.types.InlineKeyboardButton('ЭРС', callback_data='group-ЭРС')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ЭС', callback_data='group-ЭС'),
                #     )   
                #     bot.send_message(  
                #         message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
                #         reply_markup=keyboard,   
                #     parse_mode='HTML'  
                #     )
                # elif faculty_answer == "Геологоразведочный":
                #     bot.send_chat_action(message.chat.id, 'typing')
                #     keyboard = telebot.types.InlineKeyboardMarkup()  
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ГНГ', callback_data='group-ГНГ'),
                #         telebot.types.InlineKeyboardButton('МГП', callback_data='group-МГП')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('РГИ', callback_data='group-РГИ'),
                #         telebot.types.InlineKeyboardButton('РФ', callback_data='group-РФ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('РФС', callback_data='group-РФС'),
                #         telebot.types.InlineKeyboardButton('НТС', callback_data='group-НТС')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('РМ', callback_data='group-РМ'),
                #         telebot.types.InlineKeyboardButton('РГГ', callback_data='group-РГГ')  
                #     )  
                #     bot.send_message(  
                #         message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
                #         reply_markup=keyboard,   
                #     parse_mode='HTML'  
                #     )
                # elif faculty_answer == "Горный":
                #     bot.send_chat_action(message.chat.id, 'typing')
                #     keyboard = telebot.types.InlineKeyboardMarkup()  
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('БТС', callback_data='group-БТС'),
                #         telebot.types.InlineKeyboardButton('ВД', callback_data='group-ВД')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ИЗС', callback_data='group-ИЗС'),
                #         telebot.types.InlineKeyboardButton('ТО', callback_data='group-ТО')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ТПП', callback_data='group-ТПП'),
                #         types.InlineKeyboardButton('ТПР', callback_data='group-ТПР')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('БТБ', callback_data='group-БТБ'),
                #         telebot.types.InlineKeyboardButton('ИЗБ', callback_data='group-ИЗБ')  
                #     )   
                #     bot.send_message(  
                #         message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
                #         reply_markup=keyboard,   
                #     parse_mode='HTML'  
                #     )
                # elif faculty_answer == "Нефтегазовый":
                #     bot.send_chat_action(message.chat.id, 'typing')
                #     keyboard = telebot.types.InlineKeyboardMarkup()  
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('НГС', callback_data='group-НГС'),
                #         telebot.types.InlineKeyboardButton('РТ', callback_data='group-РТ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ГРП', callback_data='group-ГРП'),
                #         telebot.types.InlineKeyboardButton('ДГ', callback_data='group-НБ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('НБШ', callback_data='group-НБШ'),
                #         telebot.types.InlineKeyboardButton('НГШ', callback_data='group-НГШ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('НД', callback_data='group-НД'),
                #         telebot.types.InlineKeyboardButton('СТ', callback_data='group-СТ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ТНГ', callback_data='group-ТНГ'),
                #         telebot.types.InlineKeyboardButton('ЭХТ', callback_data='group-ЭХТ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('КРС', callback_data='group-КРС'),
                #         telebot.types.InlineKeyboardButton('НБС', callback_data='group-НБС')  
                #     )   
                #     bot.send_message(  
                #         message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
                #         reply_markup=keyboard,   
                #     parse_mode='HTML'  
                #     )
                # elif faculty_answer == "Строительный":
                #     bot.send_chat_action(message.chat.id, 'typing')
                #     keyboard = telebot.types.InlineKeyboardMarkup()  
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ГГ', callback_data='group-ГГ'),
                #         telebot.types.InlineKeyboardButton('ГС', callback_data='group-ГС')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('АГС', callback_data='group-АГС'),
                #         telebot.types.InlineKeyboardButton('ИГ', callback_data='group-ИГ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('СПС', callback_data='group-СПС'),
                #         telebot.types.InlineKeyboardButton('ГК', callback_data='group-ГК')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ПГС', callback_data='group-ПГС'),
                #     )  
                #     bot.send_message(  
                #         message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
                #         reply_markup=keyboard,   
                #     parse_mode='HTML'  
                #     )
                # elif faculty_answer == "Переработка":
                #     bot.send_chat_action(message.chat.id, 'typing')
                #     keyboard = telebot.types.InlineKeyboardMarkup()  
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ОП', callback_data='group-ОП'),
                #         telebot.types.InlineKeyboardButton('АПГ', callback_data='group-АПГ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('АПМ', callback_data='group-АПМ'),
                #         telebot.types.InlineKeyboardButton('АПН', callback_data='group-АПН')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('МЦ', callback_data='group-МЦ'),
                #         telebot.types.InlineKeyboardButton('ОНГ', callback_data='group-ОНГ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ТХ', callback_data='group-ТХ'),
                #         telebot.types.InlineKeyboardButton('ТХН', callback_data='group-ТХН')
                #     )  
                #     bot.send_message(  
                #         message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
                #         reply_markup=keyboard,   
                #     parse_mode='HTML'  
                #     )
                # elif faculty_answer == "Фундаментальные":
                #     bot.send_chat_action(message.chat.id, 'typing')
                #     keyboard = telebot.types.InlineKeyboardMarkup()  
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ИАС', callback_data='group-ИАС'),
                #         telebot.types.InlineKeyboardButton('ИСТ', callback_data='group-ИСТ')  
                #     )
                #     bot.send_message(  
                #         message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
                #         reply_markup=keyboard,   
                #     parse_mode='HTML'  
                #     )
                # elif faculty_answer == "Экономический":
                #     bot.send_chat_action(message.chat.id, 'typing')
                #     keyboard = telebot.types.InlineKeyboardMarkup()  
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('ИТУ', callback_data='group-ИТУ'),
                #         telebot.types.InlineKeyboardButton('МП', callback_data='group-МП')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('САМ', callback_data='group-САМ'),
                #         telebot.types.InlineKeyboardButton('ЭГ', callback_data='group-ЭГ')  
                #     )
                #     keyboard.add(  
                #         telebot.types.InlineKeyboardButton('БА', callback_data='group-БА'),
                #         telebot.types.InlineKeyboardButton('МТ', callback_data='group-МТ')  
                #     )
                #     bot.send_message(  
                #         message.chat.id,'Вы выбрали ' + str(faculty_answer) + ' факультет.' + '\n' + 'Выберите вашу группу',
                #         reply_markup=keyboard,   
                #     parse_mode='HTML'  
                #     )         


def get_years(message):
    for item in users:
        if message.from_user.id == item.id:
                bot.send_chat_action(message.chat.id, 'typing')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for year in array_years:
                    btn = types.KeyboardButton("Год:" + str(year))
                    markup.add(btn)
                bot.send_message(message.chat.id, text="Группы выбрана,выберите год обучения".format(message.from_user), reply_markup=markup) 



def get_semester(message):
         for item in users:
            if message.from_user.id == item.id:
                bot.send_chat_action(message.chat.id, 'typing')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for semester in array_semesters:
                    btn = types.KeyboardButton("Семестер:" + str(semester))
                    markup.add(btn)
                bot.send_message(message.chat.id, text="Выберите семестер".format(message.from_user), reply_markup=markup)


def get_document(message):
    for item in users:
        if message.from_user.id == item.id:
            with open('shablonBaza.png','rb') as photo_object:
                photo = photo_object
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_photo(message.chat.id,photo)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for baza in array_bazs:
                    btn = types.KeyboardButton(baza)
                    markup.add(btn)
                bot.send_message(message.chat.id, text="Выберите базу, если интересующуюся база отсутствует, тогда вставьте свою\nОБЯЗАТЕЛЬНО ПРОВЕРЬТЕ ЧТОБЫ ВАША БАЗА СООТВЕТСТВОВАЛА ШАБЛОНУ ФОТОГРАФИИ СВЕРХУ !".format(message.from_user), reply_markup=markup)


def get_baza(message,answer=""):
    with open(str(message.text) + ".json") as document_obj:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in count_answers:
            btn = types.KeyboardButton(answer)
            markup.add(btn)
        data = json.load(document_obj)
        for item in users:
            if message.from_user.id == item.id:
                item.data = data
                item.file_Open = True
                if len(data) < item.index + 1:
                    print("Конец базы")
                    item.file_Open = False
                else:
                    item.right_answer = data[item.index]['Ответ']
                    bot.send_message(message.chat.id, text="Выберите правильный ответ".format(message.from_user), reply_markup=markup)
                    bot.send_message(message.chat.id,
                        data[item.index]['Вопрос'] + "\n" + data[item.index]['Ответы'],   
                        parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def func(message):
    for item in users:
            if message.from_user.id == item.id:        
                if(message.text in mining_facults):
                    item.faculty = message.text
                    get_groups(message)
                    print("Вызов функции")
                elif(message.text in emf_groups):
                    item.group = message.text
                    get_years(message)
                elif("Год:" in message.text):
                    item.year = message.text[-1]
                    get_semester(message)
                elif("Семестер:" in message.text):
                    item.semester = message.text[-1]
                    get_document(message)
                elif(message.text in array_bazs):
                    item.document = message
                    get_baza(message)
                elif item.file_Open:
                    if(message.text == "1"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_baza(message = item.document,answer=message.text)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif(message.text == "2"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_baza(message = item.document,answer=message.text)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif(message.text == "3"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_baza(message = item.document,answer=message.text)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif message.text == "4":
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_baza(message = item.document,answer=message.text)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    else:
                        bot.send_message(message.chat.id, text="Ответ должен быть от 1 до 4")


bot.polling(none_stop=True)
