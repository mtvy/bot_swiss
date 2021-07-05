# Main libraries
from pickle import FALSE
import schedule, datetime, psycopg2, telebot, time, json, io, os, traceback
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Array, Process
from telebot import types

# Project files
import config, database, classes, path, variables

account_settings = database.get_accounts_data()

def openfileforRead(action=None, name_path=None, file_text='') -> str:
    return file_text.join([i for i in io.open(name_path, encoding='utf-8')])

def langCheck(message = None, person_id = None) -> bool:
    """
    This def returns True if the language is Russian.
    """
    global account_settings
    return True if account_settings[str(message.chat.id) if person_id == None else str(person_id)].language == "Русский" else False

def saveNewText(message, name_path) -> None:
    open(name_path, 'w', encoding='utf-8').write(message.text)
    bot.send_message(message.chat.id, "Изменения сохранены!")

def checkOperId(person_id, action) -> bool:
    """
    Use this method to check the role of a person.
    Parameters below described in variables.py
    
    all_ids_arr
    label_change_ids_arr        simple_oper_ids_arr
    doctor_oper_ids_arr         support_oper_ids_arr
    director_oper_ids_arr       feedback_oper_ids_arr
    collection_oper_ids_arr     collection_cash_ids_arr
    """
    return True if person_id in [pers_id for pers_id in action] else False


bot = telebot.TeleBot(config.TOKEN)


def start_process():
    Process(target = P_schedule.start_schedule, args = ()).start()
class P_schedule:
    """
    This class repost messages from the telegram channel.
    """

    def start_schedule():
        schedule.every(30).seconds.do(P_schedule.send_post)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def send_post():
        c_ex = 0
        account_settings = database.get_accounts_data()
        for account in account_settings.keys():
            try:
                bot.forward_message(int(account), variables.CHANNEL_ID, variables.MESSAGE_ID)
                time.sleep(1)
            except Exception as _:
                c_ex+=1
                continue
            try:
                if (int(time.time()) - account_settings[account].timer_conv) > 900 and account_settings[account].conversation == 'open':
                    stopConversation(message = None, lang = 0 if langCheck(message = None, person_id = account) else 1, pers_id = account)
            except Exception as _:
                pass
        if c_ex == len(account_settings):
            c_ex = 0
        else:
            try:
                bot.forward_message(281321076, variables.CHANNEL_ID, variables.MESSAGE_ID)
                variables.MESSAGE_ID += 1
            except Exception as qt:
                print(f"Error pushing news!\n\n{repr(qt)}")
                for id_er in variables.label_change_ids_arr:
                    bot.send_message(int(id_er), f"Error pushing news!\n\n{repr(qt)}")


@bot.message_handler(commands=['start'])
def welcome(message):
    global account_settings
    
    account_settings = database.get_accounts_data()

    new_account = [str(message.chat.id)]
    for account in account_settings.keys():
        if account_settings[account].telegram_id == new_account[0]:
            if account_settings[account].language == "Русский":
                if account_settings[account].personal_data == "YES":
                    bot.send_message(message.chat.id,"🔱Вы уже зарегистрированы в системе!")
                    keyboardRefMaker(message = message, lang = 0)
                elif account_settings[account].personal_data == "NO":
                    inlineMessages(markup_text = openfileforRead(None, path.first_lang), message = message, markup_arr = [["Согласен", "Согласен"], ["Отказываюсь", "Отказываюсь"]], action = False)
            elif account_settings[account].language == "Ozbek":
                if account_settings[account].personal_data == "YES":
                    bot.send_message(message.chat.id,"🔱Siz allaqachon ro'yxatdan o'tgansiz!")
                    keyboardRefMaker(message = message, lang = 1)
                elif account_settings[account].personal_data == "NO":
                    inlineMessages(markup_text = openfileforRead(None, path.second_lang), message = message, markup_arr = [["ROZIMAN", "Agree"], ["Qo'shilmayman", "Disagree"]], action = False)
            else:
                inlineMessages(markup_text = "🔱Choose language", message = message, markup_arr = [["Русский", "Русский"], ["Ozbek", "Ozbek"]], action = False)
            break
    else:
        new_account += [str(message.chat.username), str(message.chat.first_name), [], "close", "0", [], "0", "NO", None, 'close', 0]
        account = classes.Account(new_account)
        database.insert_account_data(account)
        account_settings[account.telegram_id] = account
        inlineMessages(markup_text = "🔱Choose language", message = message, markup_arr = [["Русский", "Русский"], ["Ozbek", "Ozbek"]], action = False)

@bot.message_handler(commands=['changeLabel'])
def adderNewLabel(message):
    if checkOperId(person_id = str(message.chat.id), action = variables.label_change_ids_arr):
        inlineMessages(markup_text = "Какой блок надо отредактировать?", message = message, markup_arr = variables.markup_change_label_arr, action = False)


def sendReqtoOper(message, which_oper, oper_send_text, markup):
    for oper_id in variables.action_oper_select[which_oper]:
        bot.send_message(int(oper_id), oper_send_text, reply_markup=markup)

def operKeyboardMaker(message, which_oper, lang):
    global account_settings
    global message_ids_dict
    account_settings[str(message.chat.id)].conversation = 'mid'
    variables.message_ids_dict[str(message.chat.id)] = message
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 0:
        item1 = types.KeyboardButton("🔙 Отклонить вызов оператора")
        item2 = types.KeyboardButton("❔ Инструкция")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "🙋 Включён режим переписки с оператором", reply_markup=markup)
    elif lang == 1:
        item1 = types.KeyboardButton("🔙 Operator chaqiruvini rad etish")
        item2 = types.KeyboardButton("❔ Ko'rsatma")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "🙋 Operator bilan yozishmalar rejimi yoqilgan", reply_markup=markup)
    oper_send_text = f'-------Запрос переписки!-------\nid: {message.chat.id} \nИмя: {message.chat.first_name} \nФамилия: {message.chat.last_name} \nUsername: @ {message.chat.username} \nЯзык: Русский\n----------------------------'
    oper_send_text = "-------Запрос переписки!-------\nid: "
    oper_send_text += str(message.chat.id)
    oper_send_text += "\nИмя: "
    oper_send_text += str(message.chat.first_name)
    oper_send_text += "\nФамилия: "
    oper_send_text += str(message.chat.last_name)
    oper_send_text += "\nUsername: @"
    oper_send_text += str(message.chat.username)
    oper_send_text += "\nЯзык: Русский\n----------------------------"
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Принять", callback_data=str(message.chat.id))
    markup.add(item1)
    user_id = str(message.chat.id)
    oper_id = '0'
    database.insert_new_data(user_id, oper_id, bot)
    sendReqtoOper(message, which_oper, oper_send_text, markup)
		

def dbDateSortEnter(message, action):
    send = bot.send_message(message.chat.id, '➕ Введите дату в формате ГОД-МЕСЯЦ-ДЕНЬ (2000-1-12)')
    bot.register_next_step_handler(send, dbSortEnter, action)
def dbSortEnter(message, action):
    date_text = database.getDataFromDB(date_start = message.text, action = action)
    if date_text == 0:
        bot.send_message(message.chat.id, 'Данной даты нет в базе!')
        return
    else: bot.send_message(message.chat.id, date_text)
    bot.register_next_step_handler(bot.send_message(message.chat.id, '➕ Введите номер строки по нужному имени или id'), dbIdSortEnter, action)
def dbIdSortEnter(message, action):
    id_text = database.getTextFromDB(id_text = message.text, action = action)
    bot.send_message(message.chat.id, id_text if id_text != 0 else 'Такого номера нет в базе!')
    return

def pushingLabelFromFile(message, path, path_sec):
    bot.send_message(message.chat.id, openfileforRead(None, path if langCheck(message) else path_sec).format(message.chat, bot.get_me()),parse_mode='html')

def operInit(message, action, set_act, id_check, deactivation=None):
    if checkOperId(person_id = str(message.chat.id), action = action): bot.send_message(message.chat.id, "Вы оператор!")
    else: operKeyboardMaker(message = message, which_oper = set_act, lang = 0 if langCheck(message) else 1)
        
def redirectInit(message, action):
    global account_settings

    bot.send_message(str(message.chat.id), action)
    if len(account_settings[str(message.chat.id)].tags) != 0:

        bot.send_message(str(account_settings[str(message.chat.id)].tags[0]), action)
        
        database.change_account_data(account = account_settings[account_settings[str(message.chat.id)].tags[0]], parametr = 'conversation', data = 'close')
        database.change_account_data(account = account_settings[account_settings[str(message.chat.id)].tags[0]], parametr = 'tags', data = [])        
        account_settings = database.get_accounts_data()

        keyboardRefMaker(message, 0 if langCheck(message) else 1, account_settings[str(message.chat.id)].tags[0])

    keyboardRefMaker(message, 0)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("👍", callback_data='👍'), types.InlineKeyboardButton("👎", callback_data='👎'))
    bot.send_message(account_settings[str(message.chat.id)].tags[0] if checkOperId(person_id = str(message.chat.id), action = variables.all_ids_arr) else str(message.chat.id), 'Оцените работу оператора!' if langCheck(message) else 'Operator ishini baholang!', reply_markup=markup)
        
def stopConversation(message, lang, pers_id=None, action = None):
    global account_settings
    person_id = pers_id if pers_id != None else str(message.chat.id)
    push_text = "❗ Завершение диалога" if lang == 0 or lang == 'Русский' else "❗ Muloqotni yakunlash"
    bot.send_message(person_id, push_text)
    if len(account_settings[person_id].tags) != 0:
        bot.send_message(str(account_settings[person_id].tags[0]), push_text)
            
        database.change_account_data(account = account_settings[account_settings[person_id].tags[0]], parametr = 'conversation', data = 'close')
        database.change_account_data(account = account_settings[account_settings[person_id].tags[0]], parametr = 'tags', data = [])        
        account_settings = database.get_accounts_data()

        keyboardRefMaker(None, 0 if account_settings[account_settings[person_id].tags[0]].language == "Русский" else 1, account_settings[person_id].tags[0])
    keyboardRefMaker(None, lang, person_id)

    user_id = account_settings[person_id].tags[0] if checkOperId(person_id = person_id, action = variables.all_ids_arr) and action == None else person_id
    if not checkOperId(person_id = person_id, action = variables.all_ids_arr):
        inlineMessages(markup_text = 'Оцените работу оператора!' if langCheck(person_id = user_id) else 'Operator ishini baholang!', person_id = user_id, markup_arr = [['👍', '👍'], ['👎', '👎']], action = False)
            
    database.change_account_data(account = account_settings[person_id], parametr = 'conversation', data = 'close')
    database.change_account_data(account = account_settings[person_id], parametr = 'tags', data = [])        
    account_settings = database.get_accounts_data()
            
    database.closerDataBase(person_id, bot)

def closeConversation(message):
    global account_settings
            
    database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'conversation', data = 'close')
    database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'tags', data = [])        
    account_settings = database.get_accounts_data()
            
    database.closerDataBase(str(message.chat.id), bot)

def setCollectionKeyboard(message, person_id, show_text = 'Выберите необходимый мед офис'):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("МО Гор.больница №1")
    item2 = types.KeyboardButton("МО Кушбеги")
    item3 = types.KeyboardButton("МО  Мирзо Улугбека")
    item4 = types.KeyboardButton("МО  Юнусата")
    item5 = types.KeyboardButton("МО  viezd")
    item6 = types.KeyboardButton("🔙 Назад")
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(person_id, show_text, reply_markup=markup)

def selectOffice(message, person_id, step, push_text = ''):
    if checkOperId(person_id = person_id, action = variables.collection_oper_ids_arr):
        if variables.show_text_dict[step]:
            database.dbCollection(message = message, person_id = person_id, step = step - 1, database_push_data = message.text)
            bot.send_message(person_id, variables.show_text_dict[step])
            bot.register_next_step_handler(message, selectOffice, person_id, step + 1)
        else:
            database.dbCollection(message = message, person_id = person_id, step = step - 1, database_push_data = message.text)
            data = ''.join([f"{str(row)}\n" for row in database.dbCollection(message = message, person_id = person_id, step = step, database_push_data = 'admin')])
            bot.send_message(person_id, data)
            inlineMessages(markup_text = 'Можете отправить отчёт или изменить данные', message = message, markup_arr = [['Отправить отчёт', 'Отправить отчёт'], ['Изменить', 'Изменить']])

    elif checkOperId(person_id = person_id, action = variables.collection_cash_ids_arr):
        database.dbCollection(message = message, person_id = person_id, database_push_data = message.text, action = 'cashier_init')
        data =  database.dbCollection(message = message, person_id = person_id, database_push_data = message.text, step = 9, action = 'show_collection_to_cashier')
        data = ''.join([f"{str(row)}\n" for row in data[0]]) if len(data) > 0 else 'Данных по этому офису нет!'
        bot.send_message(person_id, data)
        if data != 'Данных по этому офису нет!': inlineMessages(markup_text = 'Можете подтвердить или изменить данные', message = message, markup_arr = [['Подтвердить', 'Подтвердить'], ['Изменить', 'Изменить']])



@bot.message_handler(content_types=['text', 'photo'])
def lol(message):
    global account_settings
    global mess

    account_settings = database.get_accounts_data()
    
    #Описать Жалобу для Узбекского
    
    if message.chat.type == 'private':
        if message.text in variables.message_text_dict.keys():
            if variables.message_text_dict[message.text][0] == 'office':
                selectOffice(message = message, person_id = str(message.chat.id), step = 1)
            elif variables.message_text_dict[message.text][0] == 'text_show':
                pushingLabelFromFile(message, variables.message_text_dict[message.text][1], variables.message_text_dict[message.text][2])
            elif variables.message_text_dict[message.text][0] == 'oper_show':
                operInit(message, variables.message_text_dict[message.text][1], variables.message_text_dict[message.text][2], str(message.chat.id))
            elif variables.message_text_dict[message.text][0] == 'oper_close':
                stopConversation(message, variables.message_text_dict[message.text][1])
            elif variables.message_text_dict[message.text][0] == 'redirect':
                redirectInit(message, f"❗ Общение завершено, перенаправление {variables.message_text_dict[message.text][1]}")
                operInit(variables.message_ids_dict[account_settings[str(message.chat.id)].tags[0]], variables.message_text_dict[message.text][2], variables.message_text_dict[message.text][3], closeConversation(message))
            elif variables.message_text_dict[message.text][0] == 'discount':
                bot.send_message(message.chat.id, openfileforRead(None, variables.message_text_dict[message.text][1]).format(message.chat, bot.get_me()),parse_mode='html')
        elif message.text == '🔙 Назад':
            stopConversation(message, account_settings[str(message.chat.id)].language, action = 'back')
        elif message.text == '❗️ Оставить жалобу' or message.text == '❗️ Shikoyat qoldiring':
            if checkOperId(person_id = str(message.chat.id), action = variables.feedback_oper_ids_arr):
                dbDateSortEnter(message = message, action = 'feedback_tb')
            else:
                account_settings[str(message.chat.id)].feedback_st = 'open'
                markup = types.InlineKeyboardMarkup(row_width=2)
                button_text = "Написать жалобу" if langCheck(message) else "Shikoyat yozing"
                markup.add(types.InlineKeyboardButton(button_text, callback_data = button_text))
                bot.send_message(message.chat.id, openfileforRead(None, path.recv_label if langCheck(message) else path.sec_recv_label).format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif message.text == "💰 Инкассация":
            setCollectionKeyboard(message = message, person_id = str(message.chat.id))
        elif message.text == '💽 БД переписок' or message.text == '💽 Yozishmalar bazasi':
            if checkOperId(person_id = str(message.chat.id), action = variables.all_ids_arr):
                dbDateSortEnter(message = message, action = 'message_tb')
            else:
                bot.send_message(message.chat.id, 'У вас нет прав для чтения базы!' if langCheck(message) else "Sizda bazani o'qish huquqi yo'q!")
        elif message.text == '% Получить скидку' or message.text == '% Chegirma oling':
            oper_write = ''
            mess = 'new'
            if (account_settings[str(message.chat.id)].discount == "0" and account_settings[str(message.chat.id)].ref == "0"):
                oper_write = openfileforRead(None, path.discount_label if langCheck(message) else path.sec_discount_label) + ("\nВаш реферальный код: " if langCheck(message) else  f"\nSizning tavsiyangiz kodi: ") + str(message.chat.id)
                bot.send_message(message.chat.id, oper_write.format(message.chat, bot.get_me()),parse_mode='html')
            elif account_settings[str(message.chat.id)].ref == "10":
                database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'discount', data = '10')       
                account_settings = database.get_accounts_data()
                picPNGmaker(message)
                bot.send_message(message.chat.id, "✅ У вас максимальная скидка!" if langCheck(message) else "✅ Siz maksimal chegirma bor!")
            else:
                if account_settings[str(message.chat.id)].discount == "10":
                    picPNGmaker(message)
                    bot.send_message(message.chat.id, "✅ У вас максимальная скидка!" if langCheck(message) else "✅ Siz maksimal chegirma bor!")
                else:
                    ru_text = f"❌ Ваши друзья ещё не активировали бота!\n❌ Всего активаций {account_settings[str(message.chat.id)].ref} из 10"
                    uz_text = f"❌ Sizning do'stlaringiz hali botni faollashtirmagan!\n❌ Jami aktivatsiyalar {account_settings[str(message.chat.id)].ref} dan 10"    
                    bot.send_message(message.chat.id, ru_text if langCheck(message) else uz_text)
                    picPNGmaker(message)
        elif message.text == "❗️ Жалоба":
            redirectInit(message, "❗ Общение с оператором завершено, перенаправление в раздел жалоб")
            account_settings[account_settings[str(message.chat.id)].tags[0]].feedback_st = 'open'
            markup = types.InlineKeyboardMarkup(row_width=2) 
            markup.add(types.InlineKeyboardButton("Написать жалобу" if langCheck(message) else "Shikoyat yozing", callback_data="Написать жалобу" if langCheck(message) else "Shikoyat yozing"))
            account_settings[account_settings[str(message.chat.id)].tags[0]].feedback_st = 'open'
            bot.send_message(account_settings[str(message.chat.id)].tags[0], openfileforRead(None, path.recv_label if langCheck(message) else path.sec_recv_label).format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            closeConversation(message)        
        else:
            if account_settings[str(message.chat.id)].conversation == 'open':
                if checkOperId(person_id = str(message.chat.id), action = variables.all_ids_arr):
                    database.change_account_data(account = account_settings[account_settings[str(message.chat.id)].tags[0]], parametr = 'timer_conv', data = int(time.time()))
                    sm_id = 'Operator: '
                else:
                    database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'timer_conv', data = int(time.time()))
                    sm_id = 'User: '
      
                account_settings = database.get_accounts_data()

                if message.text != None:
                    sm_id = sm_id + message.text + '\n'
                    bot.send_message(account_settings[str(message.chat.id)].tags[0], message.text)
                elif message.caption != None:
                    sm_id = sm_id + message.caption + '\n'
                    bot.send_message(account_settings[str(message.chat.id)].tags[0], message.caption)
                if message.photo != None:
                    sm_id = sm_id + 'PHOTO\n'
                    fileID = message.photo[-1].file_id
                    file_info = bot.get_file(fileID)
                    downloaded_file = bot.download_file(file_info.file_path)
                    bot.send_photo(account_settings[str(message.chat.id)].tags[0], downloaded_file)
                database.insert_text_to_data(sm_id, str(message.chat.id), bot)



def markupMaker(action, button_text) -> types.ReplyKeyboardMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pin = [types.KeyboardButton(tag) for tag in button_text.keys() if action in button_text[tag]]
    markup.add(*pin) if action != 'user' else markup.row(pin[0], pin[1], pin[3]).row(pin[5], pin[6], pin[8]).row(pin[10]).row(pin[2], pin[7]).row(pin[4], pin[9])
    return markup

def keyboardRefMaker(message, lang, pers_id=None):
    global account_settings
    person_id = pers_id if pers_id != None else str(message.chat.id)
    markup = markupMaker(action = 'admin' if checkOperId(person_id = person_id, action = variables.collection_cash_ids_arr + variables.collection_oper_ids_arr) else 'oper' if  checkOperId(person_id = person_id, action = variables.all_ids_arr) else 'user', button_text = variables.buttons_ru_text if lang == 0 or lang == 'Русский' else variables.buttons_uz_text)
    bot.send_message(person_id, openfileforRead(None, path.FAQ_label if lang == 0 or lang == 'Русский' else path.sec_FAQ_label) if not checkOperId(person_id = person_id, action = variables.all_ids_arr) else 'Открыта клавиатура оператора!', parse_mode='html', reply_markup=markup)
    if person_id != pers_id:        
        account_settings = database.get_accounts_data()
        database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'personal_data', data = 'YES')
        account_settings = database.get_accounts_data()


def checkBlockedPeople(message, markup, pers_id):
    try:
        bot.send_message(pers_id, txt, reply_markup=markup)
    except Exception as error:
        text_push = f"User {pers_id} blocked!\n\n{repr(error)}"
        print(text_push)
        for id_er in variables.label_change_ids_arr:
            bot.send_message(int(id_er), text_push)


def fdbackName(message, lang):
    global account_settings
    name_user = message.text
    if name_user != 'stop':
        if name_user == None: name_user = 'Пользователь отправил нечитаемый объект'
        variables.feed_back[str(message.chat.id)] = {"Name" : name_user, "Username" : str(message.chat.username), "Language" : account_settings[str(message.chat.id)].language}
        send = bot.send_message(message.chat.id, '➕ Введите ваш номер телефона' if lang == 0 else '➕ Telefon raqamingizni kiriting')
        bot.register_next_step_handler(send, fdbackTele, lang)
    else:
        bot.send_message(message.chat.id, '➕ Операция отменена')
def fdbackTele(message, lang):
    tele_num = message.text
    if tele_num.isdigit() == True:
        if tele_num == None: tele_num = 'Пользователь отправил нечитаемый объект'
        variables.feed_back[str(message.chat.id)].update({"Telephone number" : tele_num})
        if lang == 0:
            bot.send_message(message.chat.id, '➕ Жалоба составляется в четыре этапа:\n1) Причина жалобы\n2) Обозначение филиала/места, где произошёл инцидент\n3) Дата инцидента\n4) Имя или опишите оппонента, с которым произошёл конфликт\n❌ Для отмены операции напишите stop')
            send = bot.send_message(message.chat.id, '➕ Напишите причину жалобы')
        else:
            bot.send_message(message.chat.id, '➕ Shikoyat tort bosqichda tuziladi:\n1) Shikoyat sababi\n2) Hodisa sodir bolgan filial/joyni belgilash\n3) Hodisa sanasi\n4) Mojaro yuz bergan raqibning nomi yoki tarifi\n❌ Operatsiyani bekor qilish uchun yozing stop')
            send = bot.send_message(message.chat.id, '➕ Shikoyat sababini yozing')
        bot.register_next_step_handler(send, fdbackReason, lang)
    elif tele_num == 'stop':
        if lang == 0:
            bot.send_message(message.chat.id, '➕ Операция отменена')
        else:
            bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
    else:
        if lang == 0:
            send = bot.send_message(message.chat.id, '➕ Введите номер телефона в формате 998999999999 или напишите stop')
        else:
            send = bot.send_message(message.chat.id, '➕ Telefon raqamingizni formatda kiriting 9997777777777 yoki yozing stop')
        bot.register_next_step_handler(send, fdbackTele, lang)
def fdbackReason(message, lang):
    reason_send = message.text
    if reason_send != 'stop':
        if reason_send == None: reason_send = 'Пользователь отправил нечитаемый объект'
        variables.feed_back[str(message.chat.id)].update({"Reason" : reason_send})
        
        if lang == 0:
            send = bot.send_message(message.chat.id, '➕ Напишите филиал/место, где произошёл инцидент')
        else:
            send = bot.send_message(message.chat.id, '➕ Hodisa sodir bolgan filial/joyni yozing')

        bot.register_next_step_handler(send, fdbackPlace, lang)
    else:
        if lang == 0:
            bot.send_message(message.chat.id, '➕ Операция отменена')
        else:
            bot.send_message(message.chat.id, '➕ Amal bekor qilindi')    
def fdbackPlace(message, lang):
    place_send = message.text
    if place_send != 'stop':
        if place_send == None: place_send = 'Пользователь отправил нечитаемый объект'
        variables.feed_back[str(message.chat.id)].update({"Place" : place_send})

        if lang == 0:
            send = bot.send_message(message.chat.id, '➕ Напишите дату инцидента')
        else:
            send = bot.send_message(message.chat.id, '➕ Hodisa tarixini yozing')
        
        bot.register_next_step_handler(send, fdbackDate, lang)
    else:
        if lang == 0:
            bot.send_message(message.chat.id, '➕ Операция отменена')
        else:
            bot.send_message(message.chat.id, '➕ Amal bekor qilindi') 
def fdbackDate(message, lang):
    date_send = message.text
    if date_send != 'stop':
        if date_send == None: date_send = 'Пользователь отправил нечитаемый объект'
        variables.feed_back[str(message.chat.id)].update({"Date" : date_send})

        if lang == 0:
            send = bot.send_message(message.chat.id, '➕ Напишите имя или опишите оппонента, с которым произошёл конфликт')
        else:
            send = bot.send_message(message.chat.id, '➕ Ismni yozing yoki ziddiyatga duch kelgan raqibni tariflang')
        
        bot.register_next_step_handler(send, fdBack_fill, lang)
    else:
        if lang == 0:
            bot.send_message(message.chat.id, '➕ Операция отменена')
        else:
            bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
def fdBack_fill(message, lang):
    global txt
    feedback_user = message.text
    if lang == 0:
        if feedback_user != '📞 Телефон' and feedback_user != '💽 БД переписок' and feedback_user !='🏠 Адреса' and feedback_user !='🌐 Соц. сети' and feedback_user !='🙋 Оператор' and feedback_user != '☎️ Тех. поддержка' and feedback_user != '✍️ Написать директору' and feedback_user !='📝 Создать заказ' and feedback_user !='❗️ Оставить жалобу' and feedback_user !='% Получить скидку' and feedback_user !='®FAQ Инструкция' and feedback_user != 'stop':
            if feedback_user == None: feedback_user = 'Пользователь отправил нечитаемый объект'
            variables.feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})

            txt = "--------ЖАЛОБА--------\n" + "id: " + str(message.chat.id) + "\nИмя: " + variables.feed_back[str(message.chat.id)]["Name"] + "\nЯзык: " + \
                account_settings[str(message.chat.id)].language + "\nПричина: " + variables.feed_back[str(message.chat.id)]["Reason"] + "\nМесто: " + \
                variables.feed_back[str(message.chat.id)]["Place"] + "\nДата: " + variables.feed_back[str(message.chat.id)]["Date"] + "\nКонфликт: " + feedback_user + "\n---------------------"

            bot.send_message(message.chat.id, '➕ Контроль сервиса лаборатории SwissLab. Мы благодарим за сделанный выбор и будем рады, если вы поможете улучшить качество нашего сервиса!\n🙋 Наш оператор свяжется с вами при необходимости!')
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Ответить", callback_data='Q' + str(message.chat.id))
            markup.add(item1)
            
            for id_p in variables.all_ids_arr:
                checkBlockedPeople(message, markup, id_p)

            oper_id = '0'
            database.insert_new_feedback_data(oper_id,  str(message.chat.id), txt, bot)
        else:
            if feedback_user != '📞 telefon' and feedback_user != '💽 Yozishmalar bazasi' and feedback_user !='🏠 manzillari' and feedback_user !='🌐 Biz ijtimoiy tarmoqlarda' and feedback_user !='🙋 Operator' and feedback_user != "☎️ O'sha.  qo'llab-quvvatlash" and feedback_user != '✍️ Direktorga yozing' and feedback_user !='📝 buyurtma yaratish' and feedback_user !='❗️ Shikoyat qoldiring' and feedback_user !='% Chegirma oling' and feedback_user !="®FAQ Ko'rsatma" and feedback_user != 'stop':
                if feedback_user == None: feedback_user = 'Пользователь отправил нечитаемый объект'
                variables.feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})

                txt = "--------ЖАЛОБА--------\n" + "id: " + str(message.chat.id) + "\nИмя: " + variables.feed_back[str(message.chat.id)]["Name"] + "\nЯзык: " + \
                    account_settings[str(message.chat.id)].language + "\nПричина: " + variables.feed_back[str(message.chat.id)]["Reason"] + "\nМесто: " + \
                    variables.feed_back[str(message.chat.id)]["Place"] + "\nДата: " + variables.feed_back[str(message.chat.id)]["Date"] + "\nКонфликт: " + feedback_user + "\n---------------------"

                bot.send_message(message.chat.id, '➕ Laboratoriya xizmatini nazorat qilish SwissLab. Biz tanlaganingiz uchun tashakkur va xizmatimiz sifatini yaxshilashga yordam bersangiz xursand bolamiz!\n🙋 Agar kerak bolsa, bizning operatorimiz sizga murojaat qiladi!')
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Ответить", callback_data='Q' + str(message.chat.id))
                markup.add(item1)

                for id_p in variables.all_ids_arr:
                    checkBlockedPeople(message, markup, id_p)

                oper_id = '0'
                database.insert_new_feedback_data(oper_id,  str(message.chat.id), txt, bot)
    
    elif feedback_user == 'stop':
        if lang == 0:
            bot.send_message(message.chat.id, '➕ Операция отменена')
        else:
            bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
    else:
        if lang == 0:
            send = bot.send_message(message.chat.id, '➕ Введите ваш отзыв в правильном формате или напишите stop')
        else:
            send = bot.send_message(message.chat.id, '➕ Iltimos, sharhingizni togri formatda kiriting yoki yozing stop')
        bot.register_next_step_handler(send, fdBack_fill, lang)


def enterTag(message):
    global account_settings
    global mess
    tags = message.text
    if mess == "new":
        database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'tags', data = [])
        mess = ""
        
        account_settings = database.get_accounts_data()

    account_settings[str(message.chat.id)].tags.append(tags)
    
    database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'tags', data = account_settings[str(message.chat.id)].tags)       

    it = len(account_settings[str(message.chat.id)].tags)
    tet = "➕ Введено "
    tet += str(it)
    tet += " из 10 пользователей"
    send = bot.send_message(message.chat.id, tet)
    if (it < 10):
        bot.register_next_step_handler(send, enterTag)
    else:
        bot.send_message(message.chat.id, "❗️ Вы получите скидку после того как пользователи активируют бота\n❗️ Если хотите изменить список друзей нажмите на /tags")
def enterTag_Sec(message):
    global account_settings
    global mess
    tags = message.text
    if mess == "new":
        database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'tags', data = [])        
        mess = ""

        account_settings = database.get_accounts_data()

    account_settings[str(message.chat.id)].tags.append(tags)
    
    database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'tags', data = account_settings[str(message.chat.id)].tags)

    it = len(account_settings[str(message.chat.id)].tags)
    tet = "➕ Kirilgan "
    tet += str(it)
    tet += " 10 foydalanuvchilar"
    send = bot.send_message(message.chat.id, tet)
    if (it < 10):
        bot.register_next_step_handler(send, enterTag_Sec)
    else:
        bot.send_message(message.chat.id, "❗️ Foydalanuvchilar botni aktivlashtirgandan so'ng chegirmaga ega bo'lasiz agar do'stlaringiz ro'yxatini o'zgartirmoqchi bo'lsangiz bosing /tags")


def picPNGmaker(message):
    global account_settings
    img_text = message.chat.first_name
    img_text += ' '
    if message.chat.last_name != None:
        img_text += message.chat.last_name
    img = Image.open('lab.png')
    idraw = ImageDraw.Draw(img)
    hd = ImageFont.truetype('Arial.ttf', size = 45)
    idraw.text((150,280), img_text, fill = 'orange', font = hd)
    img.save('newAcc.png')
    with open('newAcc.png', 'rb') as f:
        contents = f.read()
    bot.send_photo(message.chat.id, contents, caption='💳 Ваша карта' if langCheck(message) else '💳 Sizning kartangiz')
    os.remove('newAcc.png')


def refAdd(message):
    global account_settings
    ref_n = message.text    
    account_settings = database.get_accounts_data()
    ch_ref = "none"
    for k in account_settings.keys():
        if k == ref_n:
            ch_ref = "yes"
            break
    if ch_ref == "yes":
        if int(account_settings[ref_n].ref) < 10:
            account_settings[ref_n].ref = str(int(account_settings[ref_n].ref) + 1)
            
            database.change_account_data(account = account_settings[ref_n], parametr = 'ref', data = str(int(account_settings[ref_n].ref) + 1))
            account_settings = database.get_accounts_data()
            bot.send_message(message.chat.id, "✅ Спасибо за активацию!" if langCheck(message) else "✅ Faollashtirish uchun rahmat!")
            bot.send_message(ref_n, "✅ Новый пользователь активировал реферальный код!" if langCheck(message) else "✅ Yangi foydalanuvchi tavsiya kodini faollashtirdi!")
            keyboardRefMaker(message, 0 if langCheck(message) else 1)
        else:
            bot.send_message(message.chat.id, "⚠️ Активации кода закончены" if langCheck(message) else "⚠️ Kodni faollashtirish tugadi")
            keyboardRefMaker(message, 0 if langCheck(message) else 1)
    elif ref_n == "stop":
        keyboardRefMaker(message, 0 if langCheck(message) else 1)
    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, '❔ Ваш код не найден, поробуйте ещё раз или напишите - stop' if langCheck(message) else '❔ Sizning kodingiz topilmadi, yana porobuyte yoki yozing - stop'), refAdd)


def userSebdText(message):
    global account_settings
    if message.text != 'stop':
        if account_settings[account_settings[str(message.chat.id)].feedback_st].language == 'Русский':
            oper_ans = 'Ответ оператора #' + account_settings[str(message.chat.id)].feedback_st + ' на вашу жалобу!👇'
            bot.send_message(account_settings[str(message.chat.id)].feedback_st, oper_ans)
        else:  
            oper_ans = 'Sizning shikoyatingizga javob beruvchi operator #' + account_settings[str(message.chat.id)].feedback_st + ' !👇'
            bot.send_message(account_settings[str(message.chat.id)].feedback_st, oper_ans)
        if message.photo != None:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            word_user_send = bot.download_file(file_info.file_path)
            bot.send_photo(account_settings[str(message.chat.id)].feedback_st, word_user_send)
        if message.text != None or message.caption != None:
            if message.text != None: word_user_send = message.text
            else: word_user_send = message.caption
            bot.send_message(account_settings[str(message.chat.id)].feedback_st, word_user_send)
            database.insert_new_feedback_data(str(message.chat.id), account_settings[str(message.chat.id)].feedback_st, word_user_send, bot)
        bot.send_message(message.chat.id, "Сообщение отправлено!")
        
        database.change_account_data(account = account_settings[account_settings[str(message.chat.id)].feedback_st], parametr = 'feedback_st', data = 'close')
        database.change_account_data(account = account_settings[str(message.chat.id)], parametr = 'feedback_st', data = 'close')        
        account_settings = database.get_accounts_data()

    else: bot.send_message(message.chat.id, 'Операция отменена!')



def inlineMessages(markup_text, call = None, message = None, person_id = None, markup_arr = [], action = True):
    """
      need param: inline_data = [text, callback_data] to make markup
    """
    person_id = person_id if person_id != None else message.chat.id if message != None else call.message.chat.id
    if action: bot.delete_message(person_id, call.message.message_id if call != None else message.message_id)
    markup = types.InlineKeyboardMarkup(row_width = 2)
    markup.add(*[types.InlineKeyboardButton(text = row[0], callback_data = row[1]) for row in markup_arr])
    bot.send_message(person_id, markup_text, reply_markup=markup)

def handlingdbCollection(message, call):
    bot.send_message(message.chat.id, ''.join([f"{str(row)}\n" for row in database.dbCollection(message = message, person_id = message.chat.id, step = variables.call_data_office_dict[call.data][1], action = 'show_data')[0]]))
    inlineMessages(markup_text = 'Можете отправить отчёт или изменить данные', message = message, markup_arr = [['Отправить отчёт', 'Отправить отчёт'], ['Изменить', 'Изменить']])


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global account_settings
    global mess
    try:
        if call.data == 'Русский':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'language', data = 'Русский')
            
            account_settings = database.get_accounts_data()

            start_txt = openfileforRead(None, path.first_lang)

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Согласен", callback_data='Согласен')
            item2 = types.InlineKeyboardButton("Отказываюсь", callback_data='Отказываюсь')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, start_txt.format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'Отказываюсь':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Вы отказались от обработки персональных данных\n♻️ Для перезапуска бота нажмите /start")
        elif call.data == 'Согласен':
            inlineMessages(markup_text = '♻️ У вас есть реферальная ссылка?', call = call, markup_arr = [['Да', 'Да'], ['Нет', 'Нет']])

        elif call.data == 'Нет':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            keyboardRefMaker(call.message, 0)
        elif call.data == 'Да':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Отправьте код')
            bot.register_next_step_handler(send, refAdd)

        elif call.data == 'Ozbek':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'language', data = 'Ozbek')
            
            account_settings = database.get_accounts_data()

            start_txt = openfileforRead(None, path.second_lang)

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("ROZIMAN", callback_data='Agree')
            item2 = types.InlineKeyboardButton("Qo'shilmayman", callback_data='Disagree')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, start_txt.format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'Disagree':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Siz shaxsiy ma'lumotlarni qayta ishlash uchun rad qilgan\n♻️ Botni qayta ishga tushirish uchun bosing /start")
        elif call.data == 'Agree':
            inlineMessages(markup_text="♻️ Yo'naltiruvchi havola bormi?", call = call, markup_arr = [['Ha', 'Yes'], ["Yo'q", 'No']])
        elif call.data == 'No':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            keyboardRefMaker(call.message, 1)
        elif call.data == 'Yes':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Kodni yuboring')
            bot.register_next_step_handler(send, refAdd)

        elif call.data == 'Написать жалобу':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Напишите ваше имя')
            bot.register_next_step_handler(send, fdbackName, 0)
        elif call.data == 'Shikoyat yozing':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Telefon raqamingizni kiriting')
            bot.register_next_step_handler(send, fdbackName, 1)

        elif call.data == 'Отправить tag друзей':
            mess = "new"
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введено 0 из 10 пользователей')
            bot.register_next_step_handler(send, enterTag)
        elif call.data == 'Send friends @tags':
            mess = "new"
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ 10 ta foydalanuvchidan 0 ga kirgan')
            bot.register_next_step_handler(send, enterTag_Sec)

        elif call.data == 'Начальный текст':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangStart'], ['Ozbek', 'OzbekLangStart']])
        elif call.data == 'РусскийLangStart':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.first_lang)
        elif call.data == 'OzbekLangStart':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.second_lang)

        elif call.data == 'FAQ текст':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangFAQ'], ['Ozbek', 'OzbekLangFAQ']])
        elif call.data == 'РусскийLangFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.FAQ_label)
        elif call.data == 'OzbekLangFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_FAQ_label)

        elif call.data == 'Текст оператора':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangOper'], ['Ozbek', 'OzbekLangOper']])
        elif call.data == 'РусскийLangOper':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.oper_label)
        elif call.data == 'OzbekLangOper':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_oper_label)

        elif call.data == 'Текст телефона':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangTele'], ['Ozbek', 'OzbekLangTele']])
        elif call.data == 'РусскийLangTele':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.telephone_num)
        elif call.data == 'OzbekLangTele':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_telephone_num)

        elif call.data == 'Текст адресса':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangAdress'], ['Ozbek', 'OzbekLangAdress']])
        elif call.data == 'РусскийLangAdress':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.address_label)
        elif call.data == 'OzbekLangAdress':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_address_label)

        elif call.data == 'Текст создания заказа':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangOrder'], ['Ozbek', 'OzbekLangOrder']])
        elif call.data == 'РусскийLangOrder':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.order_label)
        elif call.data == 'OzbekLangOrder':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_order_label)

        elif call.data == 'Текст отзыва':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangRecv'], ['Ozbek', 'OzbekLangRecv']])
        elif call.data == 'РусскийLangRecv':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.recv_label)
        elif call.data == 'OzbekLangRecv':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_recv_label)

        elif call.data == 'Текст скидки':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangDisc'], ['Ozbek', 'OzbekLangDisc']])
        elif call.data == 'РусскийLangDisc':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.discount_label)
        elif call.data == 'OzbekLangDisc':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_discount_label)

        elif call.data == 'Текст социальные сети':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangSocial'], ['Ozbek', 'OzbekLangSocial']])
        elif call.data == 'РусскийLangSocial':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.social_web)
        elif call.data == 'OzbekLangSocial':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_social_web)

        elif call.data == 'Текст инструкции оператора':
            inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = [['Русский', 'РусскийLangOperFAQ'], ['Ozbek', 'OzbekLangOperFAQ']])
        elif call.data == 'РусскийLangOperFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path.FAQoper_label)
        elif call.data == 'OzbekLangOperFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path.sec_FAQoper_label)

        elif call.data == '👍' or call.data == '👎':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Спасибо за оценку!' if langCheck(person_id = call.message.chat.id) else 'Baholash uchun rahmat!')
            
        elif call.data == 'Изменить': 
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Номер терминала', callback_data='Номер терминала')
            item2 = types.InlineKeyboardButton('Исправить наличные', callback_data='Исправить наличные')
            item3 = types.InlineKeyboardButton('Номер договора', callback_data='Номер договора')
            item4 = types.InlineKeyboardButton('Информация по возврату средств', callback_data='Информация по возврату средств')
            item5 = types.InlineKeyboardButton('Данные по ПЦР', callback_data='Данные по ПЦР')
            item6 = types.InlineKeyboardButton('Данные по ПЦР экспресс', callback_data='Данные по ПЦР экспресс')
            item7 = types.InlineKeyboardButton('Количество анализов', callback_data='Количество анализов')
            item8 = types.InlineKeyboardButton('Комментарий', callback_data='Комментарий')
            markup.add(item1, item2, item3, item4, item5, item6, item7, item8)
            bot.send_message(call.message.chat.id, 'Что нужно исправить?', reply_markup=markup)
            
        elif call.data in variables.call_data_office_dict.keys():
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите данные для изменения")
            bot.register_next_step_handler(send, handlingdbCollection, call = call)
        elif call.data == 'Отправить отчёт':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            database.dbCollection(call.message, person_id = call.message.chat.id, action = 'send_collection_to_oper')
            bot.send_message(call.message.chat.id, 'Отчёт отправлен!')
            keyboardRefMaker(call.message, 0 if langCheck(person_id = str(call.message.chat.id)) else 1, str(call.message.chat.id))
        elif call.data == 'Подтвердить':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            database.dbCollection(call.message, person_id = call.message.chat.id, action = 'confirm_collection')
            bot.send_message(call.message.chat.id, 'Отчёт подтверждён!')
            keyboardRefMaker(call.message, 0 if langCheck(person_id = str(call.message.chat.id)) else 1, str(call.message.chat.id))
            
        elif call.data[0] == 'Q':
            if account_settings[call.data[1:]].feedback_st == 'open':
                
                database.change_account_data(account = account_settings[call.data[1:]], parametr = 'feedback_st', data = 'close')        
                database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'feedback_st', data = call.data[1:])
                account_settings = database.get_accounts_data()

                send = bot.send_message(call.message.chat.id, "➕ Введите текст для ответа пользователю")
                bot.register_next_step_handler(send, userSebdText)
            else:
                bot.send_message(call.message.chat.id, "Оператор уже ответил этому пользователю!\nДля отмены повторного ответа напишите stop")
                
                database.change_account_data(account = account_settings[call.data[1:]], parametr = 'feedback_st', data = 'close')        
                database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'feedback_st', data = call.data[1:])
                account_settings = database.get_accounts_data()

                send = bot.send_message(call.message.chat.id, "➕ Введите текст для ответа пользователю")
                bot.register_next_step_handler(send, userSebdText)
        else:
            if account_settings[str(call.message.chat.id)].conversation == 'close':
                for k in account_settings.keys():
                    if k == call.data and account_settings[k].conversation == 'mid':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton("🔙 Отклонить вызов оператора")
                        item2 = types.KeyboardButton("❔ Инструкция")
                        item3 = types.KeyboardButton("❗️ Жалоба")
                        item4 = types.KeyboardButton("🙋 Операторская")
                        item5 = types.KeyboardButton("☎️ Поддержка")
                        item6 = types.KeyboardButton("✍️ Директор")
                        item7 = types.KeyboardButton("👨‍⚕️ Доктор")
                        markup.row(item1, item2).row(item3, item4, item5).row(item6, item7)
                        account_settings[str(call.message.chat.id)].tags.append(str(k))
                        database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'tags', data = account_settings[str(call.message.chat.id)].tags)        
                        database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'conversation', data = 'open')
                        database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'timer_conv', data = int(time.time()))
                        account_settings[k].tags.append(str(call.message.chat.id))
                        account_settings[k].tags.append("0")
                        database.change_account_data(account = account_settings[k], parametr = 'tags', data = account_settings[k].tags)        
                        database.change_account_data(account = account_settings[k], parametr = 'conversation', data = 'open')
                        database.change_account_data(account = account_settings[k], parametr = 'timer_conv', data = int(time.time()))
                        account_settings = database.get_accounts_data()

                        if account_settings[k].language == "Русский":
                            oper_ans = "📞 Найден оператор #" + str(call.message.chat.id) + " , переписка активирована"
                            bot.send_message(k, oper_ans)
                        else:
                            oper_ans = "📞 Operator #" + str(call.message.chat.id) + " topildi, yozishmalar faollashtirildi"
                            bot.send_message(k, oper_ans)
                        bot.send_message(str(call.message.chat.id), "📞 Вы подтвердили заявку!", reply_markup=markup)
                        user_id = str(k)
                        oper_id = str(call.message.chat.id)
                        database.insert_new_data(user_id, oper_id, bot)
                        break
                if account_settings[str(call.message.chat.id)].conversation != 'open':
                    if account_settings[str(call.data)].conversation != 'open':
                        u_tex = "Пользователь id: "
                        u_tex += str(call.data)
                        u_tex += " отменил режим!\nПовторный вызов..."
                        bot.send_message(call.message.chat.id, u_tex)
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton("🔙 Отклонить вызов оператора")
                        item2 = types.KeyboardButton("❔ Инструкция")
                        item3 = types.KeyboardButton("❗️ Жалоба")
                        item4 = types.KeyboardButton("🙋 Операторская")
                        item5 = types.KeyboardButton("☎️ Поддержка")
                        item6 = types.KeyboardButton("✍️ Директор")
                        item7 = types.KeyboardButton("👨‍⚕️ Доктор")
                        markup.row(item1, item2).row(item3, item4, item5).row(item6, item7)
                        if account_settings[str(call.data)].language != "Русский":
                            item1 = types.KeyboardButton("🔙 Operator chaqiruvini rad etish")
                            item2 = types.KeyboardButton("❔ Ko'rsatma")
                        user_markup.add(item1, item2)
                        
                        account_settings[str(call.message.chat.id)].tags.append(str(call.data))
                        database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'tags', data = account_settings[str(call.message.chat.id)].tags)
                        database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'conversation', data = 'open')
                        database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'timer_conv', data = int(time.time()))
                        account_settings[str(call.data)].tags.append(str(call.message.chat.id))
                        database.change_account_data(account = account_settings[str(call.data)], parametr = 'tags', data = account_settings[str(call.data)].tags)
                        account_settings[str(call.data)].tags.append("0")
                        database.change_account_data(account = account_settings[str(call.data)], parametr = 'tags', data = account_settings[str(call.data)].tags)
                        database.change_account_data(account = account_settings[str(call.data)], parametr = 'conversation', data = 'open')
                        database.change_account_data(account = account_settings[str(call.data)], parametr = 'timer_conv', data = int(time.time()))
                        account_settings = database.get_accounts_data()

                        try:
                            if account_settings[str(call.data)].language == "Русский":
                                oper_ans = "📞 Оператор #" + str(call.message.chat.id) + " активировал переписку"
                                bot.send_message(str(call.data), oper_ans, reply_markup=user_markup)
                            else:
                                oper_ans = "📞 Operator #" + str(call.message.chat.id) + " yozishmalarni faollashtirdi"
                                bot.send_message(str(call.data), oper_ans, reply_markup=user_markup)
                            bot.send_message(str(call.message.chat.id), "📞 Вы подтвердили заявку!", reply_markup=markup)
                            user_id = str(call.data)
                            oper_id = str(call.message.chat.id)
                            database.insert_new_data(user_id, oper_id, bot)
                        except Exception as e:
                            database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'conversation', data = 'close')
                            database.change_account_data(account = account_settings[str(call.data)], parametr = 'tags', data = [])
                            database.change_account_data(account = account_settings[str(call.message.chat.id)], parametr = 'tags', data = [])
                            account_settings = database.get_accounts_data()
                            bot.send_message(call.message.chat.id, 'Пользователь выключил бота!')
                    else:
                        bot.send_message(str(call.message.chat.id), "Другой оператор отвечает на заявку!")
            else:
                bot.send_message(call.message.chat.id, "Закончите старый диалог, чтобы начать новый!")


    except Exception as e:
        print("Error in the 'call' part!", repr(e))
        for id_er in variables.label_change_ids_arr:
            bot.send_message(int(id_er), "Error in the 'call' part!\n\n"+ traceback.format_exc())

if __name__ == '__main__':
    start_process()
    try:
        bot.polling(none_stop=True)
    except Exception as _:
        for id_er in variables.label_change_ids_arr:
            bot.send_message(int(id_er), f"Program error!\n\n{traceback.format_exc()}")
