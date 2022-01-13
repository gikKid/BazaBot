from logging import error
import telebot
from telebot import types
import os
import json
import io
#import config
import os.path
from SearchForQuestions import get_json, shuf


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

users = []
current_users_id = []


mining_facults = ["Геологоразведочный","Горный","ЭМФ","Нефтегазовый","Строительный","Переработка","Фундаментальные","Экономический"]
emf_groups = ["AX","ГМ","ГТС","МНМ","МО","НТС","ПМК","ТОА","ТОП","ТХО","ПЭ","ТЭ","ЭРБ","ЭРС","ЭС","РСК","ПТЭ"]
geology_groups = ["ГНГ","МГП","РГИ","РФ","РФС","НТС","РМ", "РГГ"]
gorniy_groups = ["БТС","ВД","ИЗС","ТО","ТПП","ТПР","БТБ","ИЗБ"]
neftegaz_groups = ["НГС","РТ","ГРП","НБ","НБШ","НГШ","НД","СТ","ТНГ","ЭХТ","КРС","НБС","НБ","ДГ"]
stroit_groups = ["ГГ","ГС","АГС","ИГ","СПС","ГК","ПГС"]
pererabotka_groups = ["ОП","АПГ","АПМ","АПН","МЦ","ОНГ","ТХ","ТХН"]
fundamental_groups = ["ИАС","ИСТ"]
economic_groups = ["ИТУ","МП","САМ","ЭГ","БА","МТ"]
array_years = ["1","2","3","4","5"]
array_semesters = ["1","2"]
count_answers = ["1","2","3","4"]

#TOKEN = os.environ["TOKEN"]
apikey = ""

bot = telebot.TeleBot(apikey)
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

                        if os.path.exists(f"TestDocuments/{item.faculty}") == False:
                            os.mkdir(f"TestDocuments/{item.faculty}")
                        if os.path.exists(f"TestDocuments/{item.faculty}/{item.semester}") == False:
                            os.mkdir(f"TestDocuments/{item.faculty}/{item.semester}")
                        if os.path.exists(f"TestDocuments/{item.faculty}/{item.semester}/{item.year}") == False:
                            os.mkdir(f"TestDocuments/{item.faculty}/{item.semester}/{item.year}")
                        if os.path.exists(f"TestDocuments/{item.faculty}/{item.semester}/{item.year}/{item.group}") == False:
                            os.mkdir(f"TestDocuments/{item.faculty}/{item.semester}/{item.year}/{item.group}")

                        if os.path.exists(f"TestJson/{item.faculty}") == False:
                            os.mkdir(f"TestJson/{item.faculty}")
                        if os.path.exists(f"TestJson/{item.faculty}/{item.semester}") == False:
                            os.mkdir(f"TestJson/{item.faculty}/{item.semester}")
                        if os.path.exists(f"TestJson/{item.faculty}/{item.semester}/{item.year}") == False:
                            os.mkdir(f"TestJson/{item.faculty}/{item.semester}/{item.year}")
                        if os.path.exists(f"TestJson/{item.faculty}/{item.semester}/{item.year}/{item.group}") == False:
                            os.mkdir(f"TestJson/{item.faculty}/{item.semester}/{item.year}/{item.group}")

                        src =f"TestDocuments/{item.faculty}/{item.semester}/{item.year}/{item.group}/{message.document.file_name}"
                        item.document = message.document.file_name
                        with io.open(f"data_shablon.json", encoding="utf-8") as json_data_bot:
                            json_data_bot = json.load(json_data_bot) #чтение json файла в list
                            if message.document.file_name in json_data_bot[item.faculty][item.semester][item.year][item.group]:
                                bot.send_message(message.chat.id,'База с данным названием уже существует, пожалуйста поменяйте название')
                            else:
                                json_data_bot[item.faculty][item.semester][item.year][item.group].append(message.document.file_name)
                                with io.open("data_shablon.json", "w", encoding="utf-8") as data_file:
                                    json.dump(json_data_bot, data_file, ensure_ascii=False,indent=4)
                                with open(src, 'wb') as new_file:
                                    new_file.write(downloaded_file)
                                get_json(f'TestDocuments/{item.faculty}/{item.semester}/{item.year}/{item.group}/{item.document}',item=item)
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
                    btn = types.KeyboardButton("Семестр:" + str(semester))
                    markup.add(btn)
                bot.send_message(message.chat.id, text="Выберите семестр".format(message.from_user), reply_markup=markup)


def get_document(message):
    for item in users:
        if message.from_user.id == item.id:
            with open('shablonBaza.jpg','rb') as photo_object:
                photo = photo_object
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_photo(message.chat.id,photo)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Посмотреть базы")
                btn2 = types.KeyboardButton("Открыть добавленную базу")
                markup.add(btn1,btn2)
                bot.send_message(message.chat.id, text="Вставьте свою базу перед нажатием на кнопку 'Открыть добавленную базу'\n\nОБЯЗАТЕЛЬНО ПРОВЕРЬТЕ ЧТОБЫ ВАША БАЗА СООТВЕТСТВОВАЛА ШАБЛОНУ ФОТОГРАФИИ СВЕРХУ И РАСШИРЕНИЕ ФАЙЛА БЫЛО .DOCX , ТАБЛИЦА ДОЛЖНА БЫТЬ В АВТОПОДБОРЕ ПО СОДЕРЖИМОМУ! БАЗА ДОЛЖНА ИМЕТЬ ДВА СТОЛБЦА, ПЕРВУЮ СТРОКУ 'ВОПРОСЫ' И 'ОТВЕТЫ' !!!!!\n\n Ответы должны быть полностью (вместе с цифрой) выделены красным цветом\n\nНа данный момент база работает только с текстовыми файлами без формул и картинок.\n\nПо возможности база не должна содержать картинки, фото и пустых ячеек.\n\nЕсли вы сделали все правильно, но база все равно не работает, напишите /help\n\nВы также можете посмотреть уже добавленные базы\n\nДождитесь пока бот не напишет 'Документ получен', только после этого нажимайте 'Открыть добавленную базу' !".format(message.from_user), reply_markup=markup)


def look_bazs(message):
    for item in users:
        if message.from_user.id == item.id:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if os.path.exists(f"TestJson/{item.faculty}/{item.semester}/{item.year}/{item.group}"):
                with io.open("data_shablon.json", encoding="utf-8") as json_data_bot:
                    json_data_bot = json.load(json_data_bot)
                for baza in json_data_bot[item.faculty][item.semester][item.year][item.group]:
                    btn = types.KeyboardButton(baza)
                    markup.add(btn)
                bot.send_message(message.chat.id, text="Выберите базу".format(message.from_user), reply_markup=markup)
            else:
                bot.send_message(message.chat.id, text="Баз нет, добавьте базу согласно шаблону".format(message.from_user), reply_markup=markup)
def open_current_baza(message):
    for item in users:
        if message.from_user.id == item.id:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Вопросы идут по порядку")
            btn2 = types.KeyboardButton("Вопросы перемешаны")
            markup.add(btn1,btn2)
            bot.send_message(message.chat.id, text="Выберите режим показа вопросов".format(message.from_user), reply_markup=markup)

def get_baza(message,item_passed_id):
    try:
        for item in users:
            if item.id == item_passed_id:
                with open(f"TestJson/{item.faculty}/{item.semester}/{item.year}/{item.group}/table{item.document}.json") as document_obj:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for answer in count_answers:
                        btn = types.KeyboardButton(answer)
                        markup.add(btn)
                    skip_btn = types.KeyboardButton("Пропустить вопрос")
                    markup.add(skip_btn)
                    data = json.load(document_obj)
                    for item in users:
                        if item_passed_id == item.id:
                            item.data = data
                            item.file_Open = True
                            if len(data) < item.index + 1:
                                item.file_Open = False
                                item.index = 0
                                bot.send_message(message.chat.id,
                                    "База закончилась\nЧтобы добавить новую базу напишите '/start'",
                                    parse_mode='HTML')
                                look_bazs(message)
                            else:
                                item.right_answer = data[item.index]['Ответ']
                                bot.send_message(message.chat.id, text="Выберите правильный ответ".format(message.from_user), reply_markup=markup)
                                bot.send_message(message.chat.id,
                                    data[item.index]['Вопросы'] + "\n" + data[item.index]['Ответы'],
                                    parse_mode='HTML')
    except:
        bot.send_message(message.chat.id,
                            "Исправьте базу - убедитесь, что она соответствует всем требованиям и шаблону фотографии\nНапишите /start чтобы попробовать снова\nВы также можете написать нам, если есть вопросы /help\n" + str(error),
                            parse_mode='HTML')



def get_shuf_baza(message,item_passed_id):
    try:
        #current_user = User()
        for item in users:
            if item.id == item_passed_id:
                shuf(item)
                #current_user = item

                with open(f"TestJson/{item.faculty}/{item.semester}/{item.year}/{item.group}/table{item.document}shuf.json") as document_obj:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for answer in count_answers:
                        btn = types.KeyboardButton(answer)
                        markup.add(btn)
                    skip_btn = types.KeyboardButton("Пропустить вопрос")
                    markup.add(skip_btn)
                    data = json.load(document_obj)
                    for item in users:
                        if item_passed_id == item.id:
                            item.data = data
                            item.shufle_file_Open = True
                            if len(data) < item.index + 1:
                                item.shufle_file_Open = False
                                item.index = 0
                                bot.send_message(message.chat.id,
                                    "База закончилась\nЧтобы добавить новую базу напишите '/start'",
                                    parse_mode='HTML')
                                look_bazs(message)
                            else:
                                item.right_answer = data[item.index]['Ответ']
                                bot.send_message(message.chat.id, text="Выберите правильный ответ".format(message.from_user), reply_markup=markup)
                                bot.send_message(message.chat.id,
                                    data[item.index]['Вопросы'] + "\n" + data[item.index]['Ответы'],
                                    parse_mode='HTML')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id,
                            "Исправьте базу - убедитесь, что она соответствует всем требованиям и шаблону фотографии\nНапишите /start чтобы попробовать снова\nВы также можете написать нам, если есть вопросы /help" + str(error),
                            parse_mode='HTML')

@bot.message_handler(content_types=['text'])
def func(message):
    for item in users:
            if message.from_user.id == item.id:
                print(message.text)
                with io.open("data_shablon.json", encoding="utf-8") as json_data_bot:
                    json_data_bot = json.load(json_data_bot)
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
                elif("Семестр:" in message.text):
                    item.semester = message.text[-1]
                    item.allow_doc_key = True
                    get_document(message)
                elif("Посмотреть базы" in message.text):
                    look_bazs(message)
                elif("Открыть добавленную базу" in message.text):
                    if item.document != "":
                        open_current_baza(message)
                elif("Вопросы идут по порядку" in message.text):
                    if item.document != "":
                        try:
                            get_baza(message=message,item_passed_id=item.id)
                        except:
                            bot.send_message(message.chat.id,
                        "Исправьте базу - убедитесь, что она соответствует всем требованиям и шаблону фотографии\nНапишите /start чтобы попробовать снова\nВы также можете написать нам, если есть вопросы /help",
                        parse_mode='HTML')
                elif("Вопросы перемешаны" in message.text):
                    if item.document != "":
                        try:
                            get_shuf_baza(message=message,item_passed_id=item.id)
                        except Exception as e:
                            print(e)
                            bot.send_message(message.chat.id,
                        "Исправьте базу - убедитесь, что она соответствует всем требованиям и шаблону фотографии\nНапишите /start чтобы попробовать снова\nВы также можете написать нам, если есть вопросы /help",
                        parse_mode='HTML')

                elif(message.text in json_data_bot[item.faculty][item.semester][item.year][item.group]):
                    item.document = message.text
                    open_current_baza(message)
                elif item.file_Open:
                    if(message.text == "1"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_baza(message=message,item_passed_id=item.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif(message.text == "2"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_baza(message=message,item_passed_id=item.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif(message.text == "3"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_baza(message=message,item_passed_id=item.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif message.text == "4":
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_baza(message=message,item_passed_id=item.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")

                    elif(message.text == "Пропустить вопрос"):
                        item.index += 1
                        get_baza(message=message,item_passed_id=item.id)
                    else:
                        bot.send_message(message.chat.id, text="Ответ должен быть от 1 до 4")
                elif item.shufle_file_Open:
                    if(message.text == "1"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_shuf_baza(message=message,item_passed_id=item.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif(message.text == "2"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_shuf_baza(message=message,item_passed_id=item.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif(message.text == "3"):
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_shuf_baza(message=message,item_passed_id=item.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif message.text == "4":
                        if message.text in item.right_answer:
                            bot.send_message(message.chat.id, text="Ответ правильный")
                            item.index +=1
                            get_shuf_baza(message=message,item_passed_id=item.id)
                        else:
                            bot.send_message(message.chat.id, text="Ответ неправильный")
                    elif(message.text == "Пропустить вопрос"):
                        item.index += 1
                        get_shuf_baza(message=message,item_passed_id=item.id)
                    else:
                        bot.send_message(message.chat.id, text="Ответ должен быть от 1 до 4")


bot.polling(none_stop=True)
