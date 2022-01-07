import telebot
from telebot import types
from os import write
import docx
import json
import io
import pytz
import config
from SearchForQuestions import get_json

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
        self.allow_doc_key = False

users = []
current_users_id = []


mining_facults = ["Геологоразведочный","Горный","ЭМФ","Нефтегазовый","Строительный","Переработка","Фундаментальные","Экономический"]
emf_groups = ["AX","ГМ","ГТС","МНМ","МО","НТС","ПМК","ТОА","ТОП","ТХО","ПЭ","ТЭ","ЭРБ","ЭРС","ЭС"]
geology_groups = ["ГНГ","МГП","РГИ","РФ","РФС","НТС","РМ", "РГГ"]
gorniy_groups = ["БТС","ВД","ИЗС","ТО","ТПП","ТПР","БТБ","ИЗБ"]
neftegaz_groups = ["НГС","РТ","ГРП","НБ","НБШ","НГШ","НД","СТ","ТНГ","ЭХТ","КРС","НБС","НБ"]
stroit_groups = ["ГГ","ГС","АГС","ИГ","СПС","ГК","ПГС"]
pererabotka_groups = ["ОП","АПГ","АПМ","АПН","МЦ","ОНГ","ТХ","ТХН"]
fundamental_groups = ["ИАС","ИСТ"]
economic_groups = ["ИТУ","МП","САМ","ЭГ","БА","МТ"]
array_years = ["1","2","3","4","5"]
array_semesters = ["1","2"]
count_answers = ["1","2","3","4"]

dict_groups = dict()
dict_semesters = dict()
dict_facults = dict()
array_bazs_way = list()
for f in mining_facults:
    if f == "Геологоразведочный":
        for s in array_semesters:
            for y in array_years:
                dict_groups[y] = geology_groups
            dict_semesters[s] = dict_groups
        dict_facults[f] = dict_semesters
    if f == "Горный":
        for s in array_semesters:
            for y in array_years:
                dict_groups[y] = gorniy_groups
            dict_semesters[s] = dict_groups
        dict_facults[f] = dict_semesters
    if f == "ЭМФ":
        for s in array_semesters:
            for y in array_years:
                dict_groups[y] = emf_groups
            dict_semesters[s] = dict_groups
        dict_facults[f] = dict_semesters
    if f == "Нефтегазовый":
        for s in array_semesters:
            for y in array_years:
                dict_groups[y] = neftegaz_groups
            dict_semesters[s] = dict_groups
        dict_facults[f] = dict_semesters
    if f == "Строительный":
        for s in array_semesters:
            for y in array_years:
                dict_groups[y] = stroit_groups
            dict_semesters[s] = dict_groups
        dict_facults[f] = dict_semesters
    if f == "Переработка":
        for s in array_semesters:
            for y in array_years:
                dict_groups[y] = pererabotka_groups
            dict_semesters[s] = dict_groups
        dict_facults[f] = dict_semesters
    if f == "Фундаментальные":
        for s in array_semesters:
            for y in array_years:
                dict_groups[y] = fundamental_groups
            dict_semesters[s] = dict_groups
        dict_facults[f] = dict_semesters
    if f == "Экономический":
        for s in array_semesters:
            for y in array_years:
                dict_groups[y] = economic_groups
            dict_semesters[s] = dict_groups
        dict_facults[f] = dict_semesters
        array_bazs_way = dict_facults


bot = telebot.TeleBot(config.apikey)
@bot.message_handler(commands=['start'])
def start_command(message):
    user = User()
    user.id = message.from_user.id
    if user.id not in current_users_id:
        users.append(user)
        for user in users:
            if user.id not in current_users_id:
                current_users_id.append(user.id)
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
    for item in users:
        if message.from_user.id == item.id:
            if item.allow_doc_key:
                if ".docx" in message.document.file_name:
                    try:
                        file_info = bot.get_file(message.document.file_id)
                        downloaded_file = bot.download_file(file_info.file_path)
                        src = 'TestDocuments/' + message.document.file_name
                        with open(src, 'wb') as new_file:
                            new_file.write(downloaded_file)

                        bot.reply_to(message, "Документ получен...")
                    except Exception as e:
                        bot.reply_to(message, e)


def get_groups(message):
    for item in users:
        if item.id == message.from_user.id:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if item.faculty == "ЭМФ":
                for group in emf_groups:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            elif item.faculty == "Горный":
                for group in gorniy_groups:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            elif item.faculty == "Нефтегазовый":
                for group in neftegaz_groups:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            elif item.faculty == "Геологоразведочный":
                for group in geology_groups:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            elif item.faculty == "Строительный":
                for group in stroit_groups:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            elif item.faculty == "Переработка":
                for group in pererabotka_groups:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            elif item.faculty == "Фундаментальные":
                for group in fundamental_groups:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            elif item.faculty == "Экономический":
                for group in economic_groups:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            bot.send_message(message.chat.id, text="Факультет выбран, выберите свою группу".format(message.from_user), reply_markup=markup)


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
                btn1 = types.KeyboardButton("Посмотреть базы")
                btn2 = types.KeyboardButton("Открыть добавленную базу")
                markup.add(btn1,btn2)
                bot.send_message(message.chat.id, text="Вставьте свою базу или вы можете посмотреть уже добавленные базы\nОБЯЗАТЕЛЬНО ПРОВЕРЬТЕ ЧТОБЫ ВАША БАЗА СООТВЕТСТВОВАЛА ШАБЛОНУ ФОТОГРАФИИ СВЕРХУ !".format(message.from_user), reply_markup=markup)


def look_bazs(message):
    for item in users:
        if message.from_user.id == item.id:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for baza in array_bazs:
                btn = types.KeyboardButton(baza)
                markup.add(btn)
            bot.send_message(message.chat.id, text="Выберите базу".format(message.from_user), reply_markup=markup)


def get_baza(message,answer=""):
    get_json('TestDocuments/' + message.text,message.from_user.id)
    with open("table" + str(message.from_user.id) + ".json") as document_obj:
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
                    item.file_Open = False
                    item.index = 0
                else:
                    item.right_answer = data[item.index]['Ответ']
                    bot.send_message(message.chat.id, text="Выберите правильный ответ".format(message.from_user), reply_markup=markup)
                    bot.send_message(message.chat.id,
                        data[item.index]['Вопросы'] + "\n" + data[item.index]['Ответы'],   
                        parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def func(message):
    for item in users:
            if message.from_user.id == item.id:        
                if(message.text in mining_facults):
                    item.faculty = message.text
                    get_groups(message)
                elif(message.text in emf_groups):
                    item.group = message.text
                    get_years(message)
                elif(message.text in pererabotka_groups):
                    item.group = message.text
                    get_years(message)
                elif(message.text in geology_groups):
                    item.group = message.text
                    get_years(message)
                elif(message.text in neftegaz_groups):
                    item.group = message.text
                    get_years(message)
                elif(message.text in economic_groups):
                    item.group = message.text
                    get_years(message)
                elif(message.text in stroit_groups):
                    item.group = message.text
                    get_years(message)
                elif(message.text in fundamental_groups):
                    item.group = message.text
                    get_years(message)
                elif(message.text in gorniy_groups):
                    item.group = message.text
                    get_years(message)
                elif("Год:" in message.text):
                    item.year = message.text[-1]
                    get_semester(message)
                elif("Семестер:" in message.text):
                    item.semester = message.text[-1]
                    item.allow_doc_key = True
                    get_document(message)
                elif("Посмотреть базы" in message.text):
                    look_bazs(message)
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
