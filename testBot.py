import os
import os.path
import json
import io
from logging import error

import telebot
from telebot import types

from SearchForQuestions import get_json, shuf


TOKEN = os.environ["TOKEN"]
apikey = ""
bot = telebot.TeleBot(apikey)

users = []
current_users_id = []

groups = {
    "Геологоразведочный": ["ГНГ","МГП","РГИ","РФ","РФС","НТС","РМ", "РГГ"],
    "Горный": ["БТС","ВД","ИЗС","ТО","ТПП","ТПР","БТБ","ИЗБ"],
    "ЭМФ": ["AX","ГМ","ГТС","МНМ","МО","НТС","ПМК","ТОА","ТОП","ТХО","ПЭ","ТЭ","ЭРБ","ЭРС","ЭС","РСК","ПТЭ"],
    "Нефтегазовый": ["НГС","РТ","ГРП","НБ","НБШ","НГШ","НД","СТ","ТНГ","ЭХТ","КРС","НБС","НБ","ДГ"],
    "Строительный": ["ГГ","ГС","АГС","ИГ","СПС","ГК","ПГС"],
    "Переработка": ["ОП","АПГ","АПМ","АПН","МЦ","ОНГ","ТХ","ТХН"],
    "Фундаментальные": ["ИАС","ИСТ"],
    "Экономический": ["ИТУ","МП","САМ","ЭГ","БА","МТ"]
}

period = {
    "Курс": ["1","2","3","4","5"],
    "Семестр": ["1","2"]
}

array_years = ["1","2","3","4","5"]
array_semesters = ["1","2"]
count_answers = ["1","2","3","4"]


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
        self.shufle_file_Open = False
        self.allow_doc_key = False


def send_period(message, key):
    for user in users:
        if message.from_user.id == user.id:
                bot.send_chat_action(message.chat.id, 'typing')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i in period[key]:
                    btn = types.KeyboardButton(f"{key}:" + i)
                    markup.add(btn)
                bot.send_message(message.chat.id, text=f"Выберите {key}", reply_markup=markup)



def send_groups(message):
    for user in users:
        if user.id == message.from_user.id:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for group in groups[user.faculty]:
                    btn = types.KeyboardButton(group)
                    markup.add(btn)
            bot.send_message(message.chat.id, text="Факультет выбран, выберите свою группу", reply_markup=markup)


def get_document(message):
    for user in users:
        if message.from_user.id == user.id:
            with open('shablonBaza.jpg','rb') as photo_object:
                photo = photo_object
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_photo(message.chat.id,photo)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Посмотреть базы")
                btn2 = types.KeyboardButton("Открыть добавленную базу")
                markup.add(btn1,btn2)
                bot.send_message(message.chat.id, text="Вставьте свою базу перед нажатием на кнопку 'Открыть добавленную базу'\n\nОБЯЗАТЕЛЬНО ПРОВЕРЬТЕ ЧТОБЫ ВАША БАЗА СООТВЕТСТВОВАЛА ШАБЛОНУ ФОТОГРАФИИ СВЕРХУ И РАСШИРЕНИЕ ФАЙЛА БЫЛО .DOCX , ТАБЛИЦА ДОЛЖНА БЫТЬ В АВТОПОДБОРЕ ПО СОДЕРЖИМОМУ! БАЗА ДОЛЖНА ИМЕТЬ ДВА СТОЛБЦА, ПЕРВУЮ СТРОКУ 'ВОПРОСЫ' И 'ОТВЕТЫ' !!!!!\n\n Ответы должны быть полностью (вместе с цифрой) выделены красным цветом\n\nНа данный момент база работает только с текстовыми файлами без формул и картинок.\n\nПо возможности база не должна содержать картинки, фото и пустых ячеек.\n\nЕсли вы сделали все правильно, но база все равно не работает, напишите /help\n\nВы также можете посмотреть уже добавленные базы\n\nДождитесь пока бот не напишет 'Документ получен', только после этого нажимайте 'Открыть добавленную базу' !", reply_markup=markup)


def look_bazs(message):
    for user in users:
        if message.from_user.id == user.id:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if os.path.exists(f"TestJson/{user.faculty}/{user.semester}/{user.year}/{user.group}"):
                with io.open("data_shablon.json", encoding="utf-8") as json_data_bot:
                    json_data_bot = json.load(json_data_bot)
                for baza in json_data_bot[user.faculty][user.semester][user.year][user.group]:
                    btn = types.KeyboardButton(baza)
                    markup.add(btn)
                bot.send_message(message.chat.id, text="Выберите базу", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, text="Баз нет, добавьте базу согласно шаблону", reply_markup=markup)
                
                
def open_current_baza(message):
    for user in users:
        if message.from_user.id == user.id:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Вопросы идут по порядку")
            btn2 = types.KeyboardButton("Вопросы перемешаны")
            markup.add(btn1,btn2)
            bot.send_message(message.chat.id, text="Выберите режим показа вопросов", reply_markup=markup)

            
def get_baza(message, item_passed_id, is_shuf=False):
    try:
        for user in users:
            if user.id == item_passed_id:
                if is_shuf:
                    shuf(user)
                with open(f"TestJson/{user.faculty}/{user.semester}/{user.year}/{user.group}/table{user.document}.json") as document_obj:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for answer in count_answers:
                        btn = types.KeyboardButton(answer)
                        markup.add(btn)
                    skip_btn = types.KeyboardButton("Пропустить вопрос")
                    markup.add(skip_btn)
                    data = json.load(document_obj)
                    user.data = data
                    for user in users:
                        if item_passed_id == user.id:
                            user.data = data
                            user.file_Open = True
                            if len(data) < user.index + 1:
                                user.file_Open = False
                                user.index = 0
                                bot.send_message(message.chat.id,
                                    "База закончилась\nЧтобы добавить новую базу напишите '/start'",
                                    parse_mode='HTML')
                                look_bazs(message)
                            else:
                                user.right_answer = data[user.index]['Ответ']
                                bot.send_message(message.chat.id, text="Выберите правильный ответ", reply_markup=markup)
                                bot.send_message(message.chat.id,
                                    data[user.index]['Вопросы'] + "\n" + data[user.index]['Ответы'],
                                    parse_mode='HTML')
    except:
        bot.send_message(message.chat.id,
                            "Исправьте базу - убедитесь, что она соответствует всем требованиям и шаблону фотографии\nНапишите /start чтобы попробовать снова\nВы также можете написать нам, если есть вопросы /help\n" + str(error),
                            parse_mode='HTML')
        

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
    for faculty in groups.keys():
        btn = types.KeyboardButton(faculty)
        markup.add(btn)
    bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}! Выбери свой факультет", reply_markup=markup)

    
@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Сообщение поддержки', url='telegram.me/JohnGolt12')
    )
    bot.send_message(
        message.chat.id,
        'Если вы не видите вашей базы, или не можете добавить свою - напишите нам, чтобы мы исправили данную ситуацию :)',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    for user in users:
        if message.from_user.id == user.id:
            if user.allow_doc_key:
                if ".docx" in message.document.file_name:
                    try:
                        file_info = bot.get_file(message.document.file_id)
                        downloaded_file = bot.download_file(file_info.file_path)

                        if os.path.exists(f"TestDocuments/{user.faculty}") == False:
                            os.mkdir(f"TestDocuments/{user.faculty}")
                        if os.path.exists(f"TestDocuments/{user.faculty}/{user.semester}") == False:
                            os.mkdir(f"TestDocuments/{user.faculty}/{user.semester}")
                        if os.path.exists(f"TestDocuments/{user.faculty}/{user.semester}/{user.year}") == False:
                            os.mkdir(f"TestDocuments/{user.faculty}/{user.semester}/{user.year}")
                        if os.path.exists(f"TestDocuments/{user.faculty}/{user.semester}/{user.year}/{user.group}") == False:
                            os.mkdir(f"TestDocuments/{user.faculty}/{user.semester}/{user.year}/{user.group}")

                        if os.path.exists(f"TestJson/{user.faculty}") == False:
                            os.mkdir(f"TestJson/{user.faculty}")
                        if os.path.exists(f"TestJson/{user.faculty}/{user.semester}") == False:
                            os.mkdir(f"TestJson/{user.faculty}/{user.semester}")
                        if os.path.exists(f"TestJson/{user.faculty}/{user.semester}/{user.year}") == False:
                            os.mkdir(f"TestJson/{user.faculty}/{user.semester}/{user.year}")
                        if os.path.exists(f"TestJson/{user.faculty}/{user.semester}/{user.year}/{user.group}") == False:
                            os.mkdir(f"TestJson/{user.faculty}/{user.semester}/{user.year}/{user.group}")

                        src =f"TestDocuments/{user.faculty}/{user.semester}/{user.year}/{user.group}/{message.document.file_name}"
                        user.document = message.document.file_name
                        with io.open(f"data_shablon.json", encoding="utf-8") as json_data_bot:
                            json_data_bot = json.load(json_data_bot)
                            if message.document.file_name in json_data_bot[user.faculty][user.semester][user.year][user.group]:
                                bot.send_message(message.chat.id,'База с данным названием уже существует, пожалуйста поменяйте название')
                            else:
                                json_data_bot[user.faculty][user.semester][user.year][user.group].append(message.document.file_name)
                                with io.open("data_shablon.json", "w", encoding="utf-8") as data_file:
                                    json.dump(json_data_bot, data_file, ensure_ascii=False,indent=4)
                                with open(src, 'wb') as new_file:
                                    new_file.write(downloaded_file)
                                get_json(f'TestDocuments/{user.faculty}/{user.semester}/{user.year}/{user.group}/{user.document}',user=user)
                                bot.reply_to(message, "Документ получен...")
                    except Exception as e:
                        bot.reply_to(message, e)




        
@bot.message_handler(content_types=['text'])
def func(message):
    for user in users:
            if message.from_user.id == user.id:
                with io.open("data_shablon.json", encoding="utf-8") as json_data_bot:
                    json_data_bot = json.load(json_data_bot)
                if(message.text in groups.keys()):
                    user.faculty = message.text
                    send_groups(message)            
                elif message.text in groups[user.faculty]:
                    user.group = message.text
                    send_period(message, key="Курс")
                elif "Курс:" in message.text:
                    user.year = message.text[-1]
                    send_period(message, key="Семестр")
                elif("Семестр:" in message.text):
                    user.semester = message.text[-1]
                    user.allow_doc_key = True
                    get_document(message)
                elif("Посмотреть базы" in message.text):
                    look_bazs(message)
                elif("Открыть добавленную базу" in message.text):
                    if user.document != "":
                        open_current_baza(message)
                elif("Вопросы идут по порядку" or "Вопросы перемешаны" in message.text):
                    if user.document != "":
                        try:
                            if("Вопросы идут по порядку" in message.text):
                                get_baza(message=message, item_passed_id=user.id)
                            else:
                                get_baza(message=message, item_passed_id=user.id, is_shuf=True)
                        except:
                            bot.send_message(message.chat.id,
                        "Исправьте базу - убедитесь, что она соответствует всем требованиям и шаблону фотографии\nНапишите /start чтобы попробовать снова\nВы также можете написать нам, если есть вопросы /help",
                        parse_mode='HTML')
                elif(message.text in json_data_bot[user.faculty][user.semester][user.year][user.group]):
                    user.document = message.text
                    open_current_baza(message)
                elif user.shufle_file_Open or user.file_Open:
                    if message.text in "1234":
                        if message.text in user.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            user.index +=1
                            if user.shufle_file_Open:
                                get_baza(message=message, item_passed_id=user.id, is_shuf=True)
                            else:
                                get_baza(message=message, item_passed_id=user.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif message.text == "Пропустить вопрос":
                        user.index += 1
                        if user.shufle_file_Open:
                            get_baza(message=message, item_passed_id=user.id, is_shuf=True)
                        else:
                            get_baza(message=message, item_passed_id=user.id)
                    else:
                        bot.send_message(message.chat.id, text="Ответ должен быть от 1 до 4")


bot.polling(none_stop=True)
