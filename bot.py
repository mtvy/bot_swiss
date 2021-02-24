from lib import *


account_settings = database.get_accounts_data()

def openfileforRead(action=None, name_path=None):
    global account_settings
    if action == 'set':
        with open(path_acc_settings, 'r') as file_set:
            if(file_set.readline() == ""): 
                account_settings = {}
            else:
                file_set.close()
                with open(path_acc_settings, 'r') as file_set:
                    account_settings = json.load(file_set)
        return account_settings
    elif action == 'r':
        with open(path_acc_settings, 'r') as file_set:
            if(file_set.readline() == ""): 
                account_settings = {}
            else:
                file_set.close()
                with open(path_acc_settings, 'r') as file_set:
                    account_settings = json.load(file_set)
    elif action == 'w+':
        with open(path_acc_settings, 'w+') as f:
            json.dump(account_settings, f, indent='    ')
    else:
        file_text = ''
        with io.open(name_path, encoding='utf-8') as file_set:
                        for i in file_set:
                            file_text += i
        return file_text

def saveNewText(message, name_path):
    word = message.text
    with open(name_path, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")


bot = telebot.TeleBot(config.TOKEN)


def start_process(): ### Запуск Process
    _ = Process(target=P_schedule.start_schedule, args=()).start()
class P_schedule(): ### Class для работы c schedule
    def start_schedule(self): ### Запуск schedule
        
        ### Параметры для schedule
        schedule.every(30).seconds.do(P_schedule.send_post)

        ### Запуск цикла
        while True:
            schedule.run_pending()
            time.sleep(1)
    def send_post(self): ### Функции для выполнения заданий по времени
        global MESSAGE_ID
        global account_settings
        global message_ids_dict
        c_ex = 0

        account_settings = database.get_accounts_data()

        for account in account_settings.keys():
            try:
                time_checker = int(time.time()) - account_settings[account].timer_conv
                if time_checker > 900 and account_settings[account].conversation == 'open':
                    if account_settings[account].language == 'Русский':
                        stopConversation(None, 0, account)
                    else:
                        stopConversation(None, 1, account)
            except Exception as _:
                pass
            try:
                bot.forward_message(int(account), -1001229753165, MESSAGE_ID)
            except Exception as _:
                c_ex+=1
                continue
        if c_ex == len(account_settings):
            c_ex = 0
        else:
            try:
                bot.forward_message(281321076, -1001229753165, MESSAGE_ID)
                MESSAGE_ID += 1
            except Exception as qt:
                print("Error pushing news!", repr(qt))
                for id_er in label_change_ids_arr:
                    bot.send_message(int(id_er), "Error pushing news!" + repr(qt))


@bot.message_handler(commands=['start'])
def welcome(message):
    global account_settings
    
    account_settings = database.get_accounts_data()

    new_account = [str(message.chat.id)]
    for account in account_settings.keys():
        if account_settings[account].telegram_id == new_account[0]:
            start_txt=''
            if account_settings[account].language == "Русский":
                if account_settings[account].personal_data == "YES":
                    bot.send_message(message.chat.id,"🔱Вы уже зарегистрированы в системе!")
                    keyboardRefMaker(message, 0)
                elif account_settings[account].personal_data == "NO":

                    start_txt = openfileforRead(None, path_first_lang)
                    
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton("Согласен", callback_data='Согласен')
                    item2 = types.InlineKeyboardButton("Отказываюсь", callback_data='Отказываюсь')
                    markup.add(item1, item2)
                    bot.send_message(message.chat.id, start_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            else:
                if account_settings[account].personal_data == "YES":
                    bot.send_message(message.chat.id,"🔱Siz allaqachon ro'yxatdan o'tgansiz!")
                    keyboardRefMaker(message, 1)
                elif account_settings[account].personal_data == "NO":

                    start_txt = openfileforRead(None, path_second_lang)
                    
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = types.InlineKeyboardButton("ROZIMAN", callback_data='Agree')
                    item2 = types.InlineKeyboardButton("Qo'shilmayman", callback_data='Disagree')
                    markup.add(item1, item2)
                    bot.send_message(message.chat.id, start_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            break
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Русский", callback_data='Русский')
        item2 = types.InlineKeyboardButton("Ozbek", callback_data="Ozbek")
        markup.add(item1, item2)
        
        new_account += [str(message.chat.username), str(message.chat.first_name), [], "close", "0", [], "0", "NO", None, 'close']
        
        account = classes.Account(new_account)
        database.insert_account_data(account)
        account_settings[account.telegram_id] = account

        bot.send_message(message.chat.id,"🔱Choose language", reply_markup=markup)

@bot.message_handler(commands=['changeLabel'])
def adderNewLabel(message):
    if checkOperId(str(message.chat.id), 'check_label_changer'):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Начальный текст", callback_data='Начальный текст')
        item2 = types.InlineKeyboardButton("FAQ текст", callback_data='FAQ текст')
        item3 = types.InlineKeyboardButton("Текст оператора", callback_data='Текст оператора')
        item4 = types.InlineKeyboardButton("Текст инструкции оператора", callback_data='Текст инструкции оператора')
        item5 = types.InlineKeyboardButton("Текст телефона", callback_data='Текст телефона')
        item6 = types.InlineKeyboardButton("Текст адресса", callback_data='Текст адресса')
        item7 = types.InlineKeyboardButton("Текст создания заказа", callback_data='Текст создания заказа')
        item8 = types.InlineKeyboardButton("Текст отзыва", callback_data='Текст отзыва')
        item9 = types.InlineKeyboardButton("Текст скидки", callback_data='Текст скидки')
        item10 = types.InlineKeyboardButton("Текст социальные сети", callback_data='Текст социальные сети')
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
        bot.send_message(message.chat.id,"Какой блок надо отредактировать?", reply_markup=markup)


def sendReqtoOper(message, which_oper, oper_send_text, markup):
    if which_oper == 'simple_oper':
        for oper_id in simple_oper_ids_arr:
            bot.send_message(int(oper_id), oper_send_text, reply_markup=markup)
    elif which_oper == 'doc_oper':
        for oper_id in doctor_oper_ids_arr:
            bot.send_message(int(oper_id), oper_send_text, reply_markup=markup)
    elif which_oper == 'dir_oper':
        for oper_id in director_oper_ids_arr:
            bot.send_message(int(oper_id), oper_send_text, reply_markup=markup)
    elif which_oper == 'sup_oper':
        for oper_id in support_oper_ids_arr:
            bot.send_message(int(oper_id), oper_send_text, reply_markup=markup)

def operKeyboardMaker(message, which_oper, lang):
    global account_settings
    global message_ids_dict
    account_settings[str(message.chat.id)].conversation = 'mid'
    message_ids_dict[str(message.chat.id)] = message
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
		

def dbDateSortEnter(message):
    send = bot.send_message(message.chat.id, '➕ Введите дату в формате ГОД-МЕСЯЦ-ДЕНЬ (2000-1-12)')
    bot.register_next_step_handler(send, dbSortEnter)
def feedBackdbDateSortEnter(message):
    send = bot.send_message(message.chat.id, '➕ Введите дату в формате ГОД-МЕСЯЦ-ДЕНЬ (2000-1-12)')
    bot.register_next_step_handler(send, FeedBackdbSortEnter)


def dbSortEnter(message):
    date_text = message.text
    date_text = database.getDataFromDB(date_text, bot)
    if date_text == '0':
        bot.send_message(message.chat.id, 'Данной даты нет в базе!')
        return
    else: bot.send_message(message.chat.id, date_text)
    send = bot.send_message(message.chat.id, '➕ Введите номер строки по нужному имени или id')
    bot.register_next_step_handler(send, dbIdSortEnter)
def FeedBackdbSortEnter(message):
    date_text = message.text
    date_text = database.getDataFromFeedBackDB(date_text, bot)
    if date_text == '0':
        bot.send_message(message.chat.id, 'Данной даты нет в базе!')
        return
    else: bot.send_message(message.chat.id, date_text)
    send = bot.send_message(message.chat.id, '➕ Введите номер строки по нужному имени или id')
    bot.register_next_step_handler(send, FeedBackdbIdSortEnter)

def dbIdSortEnter(message):
    id_text = message.text
    id_text = database.getTextFromDB(id_text, bot)
    if id_text == '0':
        bot.send_message(message.chat.id, 'Такого номера нет в базе!')
        return
    else: bot.send_message(message.chat.id, id_text)
def FeedBackdbIdSortEnter(message):
    id_text = message.text
    id_text = database.getTextFromFeedBackDB(id_text, bot)
    if id_text == '0':
        bot.send_message(message.chat.id, 'Такого номера нет в базе!')
        return
    else: bot.send_message(message.chat.id, id_text)


def pushingLabelFromFile(message, path, path_sec):
    label_text = ''
    if account_settings[str(message.chat.id)].language == "Русский":
        label_text = openfileforRead(None, path)
    else:
        label_text = openfileforRead(None, path_sec)
    bot.send_message(message.chat.id, label_text.format(message.chat, bot.get_me()),parse_mode='html')

def operInit(message, action, set_act, id_check, deactivation=None):
    if checkOperId(str(message.chat.id), action):
        if account_settings[str(message.chat.id)].language == "Русский":
            operKeyboardMaker(message, set_act, 0)
        else:
            operKeyboardMaker(message, set_act, 1)
    else:
        bot.send_message(message.chat.id, "Вы оператор!")
        
def redirectInit(message, action):
    bot.send_message(str(message.chat.id), action)
    if len(account_settings[str(message.chat.id)].tags) != 0:

        bot.send_message(str(account_settings[str(message.chat.id)].tags[0]), action)
        account_settings[account_settings[str(message.chat.id)].tags[0]].conversation = 'close'
        account_settings[account_settings[str(message.chat.id)].tags[0]].tags.clear()
                
        #change_account_data(account=, parametr, data)
        #database.insert_account_data(account)
        #account_settings[account.telegram_id] = account
        #openfileforRead('r')

        if account_settings[account_settings[str(message.chat.id)].tags[0]].language == "Русский":
            keyboardRefMaker(message, 0, account_settings[str(message.chat.id)].tags[0])
        else:
            keyboardRefMaker(message, 1, account_settings[str(message.chat.id)].tags[0])

    keyboardRefMaker(message, 0)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("👍", callback_data='👍')
    item2 = types.InlineKeyboardButton("👎", callback_data="👎")
    markup.add(item1, item2)
    if checkOperId(str(message.chat.id), 'check_all_oper'):
        if account_settings[account_settings[str(message.chat.id)].tags[0]].language == "Русский":
            bot.send_message(account_settings[str(message.chat.id)].tags[0], 'Оцените работу оператора!', reply_markup=markup)
        else: bot.send_message(account_settings[str(message.chat.id)].tags[0], 'Operator ishini baholang!', reply_markup=markup)
    else:
        if account_settings[str(message.chat.id)].language == "Русский":
                    bot.send_message(str(message.chat.id), 'Оцените работу оператора!', reply_markup=markup)
        else: bot.send_message(str(message.chat.id), 'Operator ishini baholang!', reply_markup=markup)
        
def stopConversation(message, lang, pers_id=None):
    if pers_id!=None:
        person_id = pers_id
    else:
        person_id = str(message.chat.id)
    if lang == 0: 
        push_text = "❗ Общение с оператором завершено"
    else:
        push_text = "❗ Operator bilan aloqa yakunlandi"

    bot.send_message(person_id, push_text)
    if len(account_settings[person_id].tags) != 0:
        bot.send_message(str(account_settings[person_id].tags[0]), push_text)
        account_settings[account_settings[person_id].tags[0]].conversation = 'close'
        account_settings[account_settings[person_id].tags[0]].tags.clear()
            
        openfileforRead('w+')
        openfileforRead('r')
        if account_settings[account_settings[person_id].tags[0]].language == "Русский":
            keyboardRefMaker(None, 0, account_settings[person_id].tags[0])
        else:
            keyboardRefMaker(None, 1, account_settings[person_id].tags[0])
    keyboardRefMaker(None, lang, person_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("👍", callback_data='👍')
    item2 = types.InlineKeyboardButton("👎", callback_data="👎")
    markup.add(item1, item2)
    if checkOperId(person_id, 'check_all_oper'):
        if account_settings[account_settings[person_id].tags[0]].language == "Русский":
            bot.send_message(account_settings[person_id].tags[0], 'Оцените работу оператора!', reply_markup=markup)
        else: bot.send_message(account_settings[person_id].tags[0], 'Operator ishini baholang!', reply_markup=markup)
    else:
        if account_settings[person_id].language == "Русский":
            bot.send_message(person_id, 'Оцените работу оператора!', reply_markup=markup)
        else: bot.send_message(person_id, 'Operator ishini baholang!', reply_markup=markup)
    account_settings[person_id].conversation = 'close'
    account_settings[person_id].tags.clear()
            
    openfileforRead('w+')
    openfileforRead('r')
            
    database.closerDataBase(person_id, bot)

def closeConversation(message):
    global account_settings
    account_settings[str(message.chat.id)].conversation = 'close'
    account_settings[str(message.chat.id)].tags.clear()
            
    openfileforRead('w+')
    openfileforRead('r')
            
    database.closerDataBase(str(message.chat.id), bot)

@bot.message_handler(content_types=['text', 'photo'])
def lol(message):
    global account_settings
    global message_ids_dict
    global mess
    global feed_back
    openfileforRead('r')
    if message.chat.type == 'private':
        if message.text == '📞 Телефон' or message.text == '📞 telefon':
            pushingLabelFromFile(message, path_telephone_num, path_sec_telephone_num)
        elif message.text == '🏠 Адреса' or message.text == '🏠 manzillari':
            pushingLabelFromFile(message, path_address_label, path_sec_address_label)
        elif message.text == "🌐 Соц. сети" or message.text == '🌐 Biz ijtimoiy tarmoqlarda':
            pushingLabelFromFile(message, path_social_web, path_sec_social_web)
        elif message.text == '®FAQ Инструкция' or message.text == "®FAQ Ko'rsatma":
            pushingLabelFromFile(message, path_FAQ_label, path_sec_FAQ_label)
        elif message.text == '📝 Создать заказ' or message.text == '📝 buyurtma yaratish':
            pushingLabelFromFile(message, path_order_label, path_sec_order_label)
        elif message.text == '🙋 Оператор' or message.text == '🙋 Operator':
            operInit(message, 'check_simple_oper', 'simple_oper', str(message.chat.id))
        elif message.text == '👨‍⚕️ Доктор онлайн' or message.text == '👨‍⚕️ Shifokor onlayn':
            operInit(message, 'check_doc_id', 'doc_oper', str(message.chat.id))
        elif message.text == '☎️ Тех. поддержка' or message.text == '☎️ Тех. поддержка':
            operInit(message, 'check_support_id', 'sup_oper', str(message.chat.id))
        elif message.text == '✍️ Написать директору' or message.text == '✍️ Direktorga yozing':
            operInit(message, 'check_director_id', 'dir_oper', str(message.chat.id))
        elif message.text == '❗️ Оставить жалобу' or message.text == '❗️ Shikoyat qoldiring':
            if checkOperId(str(message.chat.id), 'check_feedback_oper_id'):
                oper_write = ''
                account_settings[str(message.chat.id)].feedback_st = 'open'
                markup = types.InlineKeyboardMarkup(row_width=2)
                if account_settings[str(message.chat.id)].language == "Русский":

                    oper_write = openfileforRead(None, path_recv_label)
 
                    item1 = types.InlineKeyboardButton("Написать жалобу", callback_data='Написать жалобу')
                else:

                    oper_write = openfileforRead(None, path_sec_recv_label)

                    item1 = types.InlineKeyboardButton("Shikoyat yozing", callback_data='Write a feedback')
                markup.add(item1)
                account_settings[str(message.chat.id)].feedback_st = 'open'
                bot.send_message(message.chat.id, oper_write.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            else:
                feedBackdbDateSortEnter(message)
        elif message.text == '💽 БД переписок' or message.text == '💽 Yozishmalar bazasi':
            if checkOperId(str(message.chat.id), 'check_all_oper'):
                dbDateSortEnter(message)
            else:
                if account_settings[str(message.chat.id)].language == "Русский":
                    bot.send_message(message.chat.id, 'У вас нет прав для чтения базы!')
                else: bot.send_message(message.chat.id, "Sizda bazani o'qish huquqi yo'q!")
        elif message.text == '% Получить скидку' or message.text == '% Chegirma oling':
            oper_write = ''
            mess = 'new'
            if (account_settings[str(message.chat.id)].discount == "0" and account_settings[str(message.chat.id)].ref == "0"):
                markup = types.InlineKeyboardMarkup(row_width=2)
                if account_settings[str(message.chat.id)].language == "Русский":

                    oper_write = openfileforRead(None, path_discount_label)

                    oper_write += "\nВаш реферальный код: "
                    oper_write += str(message.chat.id)
                    bot.send_message(message.chat.id, oper_write.format(message.chat, bot.get_me()),parse_mode='html')
                else:

                    oper_write = openfileforRead(None, path_sec_discount_label)

                    oper_write += "\nSizning tavsiyangiz kodi: "
                    oper_write += str(message.chat.id)
                    bot.send_message(message.chat.id, oper_write.format(message.chat, bot.get_me()),parse_mode='html')
            elif account_settings[str(message.chat.id)].ref == "10":
                account_settings[str(message.chat.id)].discount = "10"
                
                openfileforRead('w+')
                openfileforRead('r')

                if account_settings[str(message.chat.id)].language == "Русский":
                    picPNGmaker(message)
                    bot.send_message(message.chat.id, "✅ У вас максимальная скидка!")
                else:
                    picPNGmaker(message)
                    bot.send_message(message.chat.id, "✅ Siz maksimal chegirma bor!")
            else:
                if account_settings[str(message.chat.id)].language == "Русский":
                    if account_settings[str(message.chat.id)].discount == "10":
                        picPNGmaker(message)
                        bot.send_message(message.chat.id, "✅ У вас максимальная скидка!")
                    else:
                        text_tags = "❌ Ваши друзья ещё не активировали бота!\n❌ Всего активаций "
                        text_tags += account_settings[str(message.chat.id)].ref
                        text_tags += " из 10"
                        bot.send_message(message.chat.id, text_tags)
                        picPNGmaker(message)
                else:
                    if account_settings[str(message.chat.id)].discount == "10":
                        picPNGmaker(message)
                        bot.send_message(message.chat.id, "✅ Siz maksimal chegirma bor!")
                    else:
                        text_tags = "❌ Sizning do'stlaringiz hali botni faollashtirmagan!\n❌ Jami aktivatsiyalar "
                        text_tags += account_settings[str(message.chat.id)].ref
                        text_tags += " dan 10"
                        bot.send_message(message.chat.id, text_tags)
                        picPNGmaker(message)
        elif message.text == "🔙 Отклонить вызов оператора":
            stopConversation(message, 0)
        elif message.text == "🔙 Operator chaqiruvini rad etish":
            bot.send_message(str(message.chat.id), "❗ Operator bilan aloqa yakunlandi")
            stopConversation(message, 1)
        elif message.text == "❗️ Жалоба":
            
            redirectInit(message, "❗ Общение с оператором завершено, перенаправление в раздел жалоб")

            oper_write = ''
            account_settings[account_settings[str(message.chat.id)].tags[0]].feedback_st = 'open'
            markup = types.InlineKeyboardMarkup(row_width=2)
            if account_settings[account_settings[str(message.chat.id)].tags[0]].language == "Русский":

                oper_write = openfileforRead(None, path_recv_label)
 
                item1 = types.InlineKeyboardButton("Написать жалобу", callback_data='Написать жалобу')
            else:

                oper_write = openfileforRead(None, path_sec_recv_label)

                item1 = types.InlineKeyboardButton("Shikoyat yozing", callback_data='Write a feedback')
            markup.add(item1)
            account_settings[account_settings[str(message.chat.id)].tags[0]].feedback_st = 'open'
            bot.send_message(account_settings[str(message.chat.id)].tags[0], oper_write.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            closeConversation(message)        
        elif message.text == "🙋 Операторская":
            redirectInit(message, "❗ Общение завершено, перенаправление к оператору")
            operInit(message_ids_dict[account_settings[str(message.chat.id)].tags[0]], 'check_simple_oper', 'simple_oper', closeConversation(message)) 
        elif message.text == "☎️ Поддержка":
            redirectInit(message, "❗ Общение завершено, перенаправление в тех.поддержку")
            operInit(message_ids_dict[account_settings[str(message.chat.id)].tags[0]], 'check_support_id', 'sup_oper', closeConversation(message)) 
        elif message.text == "✍️ Директор":
            redirectInit(message, "❗ Общение завершено, перенаправление к директору")
            operInit(message_ids_dict[account_settings[str(message.chat.id)].tags[0]], 'check_director_id', 'dir_oper', closeConversation(message))    
        elif message.text == "👨‍⚕️ Доктор":
            redirectInit(message, "❗ Общение завершено, перенаправление к доктору")
            operInit(message_ids_dict[account_settings[str(message.chat.id)].tags[0]], 'check_doc_id', 'doc_oper', closeConversation(message))
        elif message.text == "❔ Инструкция":
            FAQ_txt = ''

            FAQ_txt = openfileforRead(None, path_FAQoper_label)
            
            bot.send_message(message.chat.id, FAQ_txt.format(message.chat, bot.get_me()),parse_mode='html')
        elif message.text == "❔ Ko'rsatma":
            FAQ_txt = ''

            FAQ_txt = openfileforRead(None, path_sec_FAQoper_label)

            bot.send_message(message.chat.id, FAQ_txt.format(message.chat, bot.get_me()),parse_mode='html')
        else:
            if account_settings[str(message.chat.id)]['conversation'] == 'open':
                if checkOperId(str(message.chat.id), 'check_all_oper'):
                    account_settings[account_settings[str(message.chat.id)].tags[0]].timer_conv = int(time.time())
                    sm_id = 'Operator: '
                else: 
                    account_settings[str(message.chat.id)].timer_conv = int(time.time())
                    sm_id = 'User: '
                openfileforRead('w+')
                openfileforRead('r')
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


def checkOperId(person_id, action):
    if action == 'check_all_oper':
        for pers_id in all_ids_arr:
            if person_id == pers_id:
                return True
        return False
    elif action == 'check_simple_oper':
        for pers_id in simple_oper_ids_arr:
            if person_id == pers_id:
                return False
        return True
    elif action == 'check_doc_id':
        for pers_id in doctor_oper_ids_arr:
            if person_id == pers_id:
                return False
        return True
    elif action == 'check_support_id':
        for pers_id in support_oper_ids_arr:
            if person_id == pers_id:
                return False
        return True
    elif action == 'check_feedback_oper_id':
        for pers_id in feedback_oper_ids_arr:
            if person_id == pers_id:
                return False
        return True
    elif action == 'check_director_id':
        for pers_id in director_oper_ids_arr:
            if person_id == pers_id:
                return False
        return True
    elif action == 'check_label_changer':
        for pers_id in label_change_ids_arr:
            if person_id == pers_id:
                return True
        return False
    

def keyboardRefMaker(message, lang, pers_id=None):
    global account_settings
    if pers_id != None:
        person_id = pers_id
    else:
        person_id = str(message.chat.id)
    if lang == 0:
        if checkOperId(person_id, 'check_all_oper'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("📞 Телефон")
            item2 = types.KeyboardButton("🏠 Адреса")
            item4 = types.KeyboardButton("📝 Создать заказ")
            item5 = types.KeyboardButton("❗️ Оставить жалобу")
            item10 = types.KeyboardButton("💽 БД переписок")
            item6 = types.KeyboardButton("% Получить скидку")
            item7 = types.KeyboardButton("®FAQ Инструкция")
            item9 = types.KeyboardButton("🌐 Соц. сети")
            markup.add(item1, item2, item4, item9, item5, item10, item6, item7)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("📞 Телефон")
            item2 = types.KeyboardButton("🏠 Адреса")
            item3 = types.KeyboardButton("🙋 Оператор")
            item4 = types.KeyboardButton("📝 Создать заказ")
            item5 = types.KeyboardButton("❗️ Оставить жалобу")
            item6 = types.KeyboardButton("% Получить скидку")
            item7 = types.KeyboardButton("®FAQ Инструкция")
            item8 = types.KeyboardButton("✍️ Написать директору")
            item9 = types.KeyboardButton("🌐 Соц. сети")
            item10 = types.KeyboardButton("☎️ Тех. поддержка")
            item11 = types.KeyboardButton("👨‍⚕️ Доктор онлайн")
            markup.row(item1, item2, item4).row(item6, item7, item9).row(item11).row(item3, item8).row(item5, item10)
        faq_txt = ''

        faq_txt = openfileforRead(None, path_FAQ_label)
        
        if person_id == pers_id:
            bot.send_message(person_id, faq_txt, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, faq_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            openfileforRead('r')
            account_settings[str(message.chat.id)].personal_data = "YES"
            openfileforRead('w+')
            openfileforRead('r')
    else:
        if checkOperId(person_id, 'check_all_oper'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("📞 telefon")
            item2 = types.KeyboardButton("🏠 manzillari")
            item4 = types.KeyboardButton("📝 buyurtma yaratish")
            item5 = types.KeyboardButton("❗️ Shikoyat qoldiring")
            item10 = types.KeyboardButton("💽 Yozishmalar bazasi")
            item6 = types.KeyboardButton("% Chegirma oling")
            item7 = types.KeyboardButton("®FAQ Ko'rsatma")
            item9 = types.KeyboardButton("🌐 Biz ijtimoiy tarmoqlarda")
            markup.add(item1, item2, item4, item9, item5, item10, item6, item7)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("📞 telefon")
            item2 = types.KeyboardButton("🏠 manzillari")
            item3 = types.KeyboardButton("🙋 Operator")
            item4 = types.KeyboardButton("📝 buyurtma yaratish")
            item5 = types.KeyboardButton("❗️ Shikoyat qoldiring")
            item6 = types.KeyboardButton("% Chegirma oling")
            item7 = types.KeyboardButton("®FAQ Ko'rsatma")
            item8 = types.KeyboardButton("✍️ Direktorga yozing")
            item9 = types.KeyboardButton("🌐 Biz ijtimoiy tarmoqlarda")
            item10 = types.KeyboardButton("☎️ O'sha.  qo'llab-quvvatlash")
            item11 = types.KeyboardButton("👨‍⚕️ Shifokor onlayn")
            markup.row(item1, item2, item4).row(item6, item7, item9).row(item11).row(item3, item8).row(item5, item10)
        faq_txt = ''

        faq_txt = openfileforRead(None, path_sec_FAQ_label)

        if person_id == pers_id:
            bot.send_message(person_id, faq_txt, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, faq_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            openfileforRead('r')
            account_settings[str(message.chat.id)].personal_data = "YES"
            openfileforRead('w+')
            openfileforRead('r')


def checkBlockedPeople(message, markup, pers_id):
    try:
        bot.send_message(pers_id, txt, reply_markup=markup)
    except Exception as e:
        text_push = 'User ' + pers_id + ' blocked!\n\n' + repr(e)
        print(text_push)
        for id_er in label_change_ids_arr:
            bot.send_message(int(id_er), text_push)
        


def fdbackName(message, lang):
    global feed_back
    global account_settings
    name_user = message.text
    if name_user != 'stop':
        if name_user == None: name_user = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)] = {"Name" : name_user, "Username" : str(message.chat.username), "Language" : account_settings[str(message.chat.id)].language}
        if lang == 0:
            send = bot.send_message(message.chat.id, '➕ Введите ваш номер телефона')
        else:
            send = bot.send_message(message.chat.id, '➕ Telefon raqamingizni kiriting')
        bot.register_next_step_handler(send, fdbackTele, lang)
    else:
        bot.send_message(message.chat.id, '➕ Операция отменена')
def fdbackTele(message, lang):
    global feed_back
    tele_num = message.text
    if tele_num.isdigit() == True:
        if tele_num == None: tele_num = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Telephone number" : tele_num})
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
    global feed_back
    reason_send = message.text
    if reason_send != 'stop':
        if reason_send == None: reason_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Reason" : reason_send})
        
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
    global feed_back
    place_send = message.text
    if place_send != 'stop':
        if place_send == None: place_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Place" : place_send})

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
    global feed_back
    date_send = message.text
    if date_send != 'stop':
        if date_send == None: date_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Date" : date_send})

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
    global feed_back
    global txt
    feedback_user = message.text
    if lang == 0:
        if feedback_user != '📞 Телефон' and feedback_user != '💽 БД переписок' and feedback_user !='🏠 Адреса' and feedback_user !='🌐 Соц. сети' and feedback_user !='🙋 Оператор' and feedback_user != '☎️ Тех. поддержка' and feedback_user != '✍️ Написать директору' and feedback_user !='📝 Создать заказ' and feedback_user !='❗️ Оставить жалобу' and feedback_user !='% Получить скидку' and feedback_user !='®FAQ Инструкция' and feedback_user != 'stop':
            if feedback_user == None: feedback_user = 'Пользователь отправил нечитаемый объект'
            feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})

            txt = "--------ЖАЛОБА--------\n" + "id: " + str(message.chat.id) + "\nИмя: " + feed_back[str(message.chat.id)]["Name"] + "\nЯзык: " + \
                account_settings[str(message.chat.id)].language + "\nПричина: " + feed_back[str(message.chat.id)]["Reason"] + "\nМесто: " + \
                feed_back[str(message.chat.id)]["Place"] + "\nДата: " + feed_back[str(message.chat.id)]["Date"] + "\nКонфликт: " + feedback_user + "\n---------------------"

            bot.send_message(message.chat.id, '➕ Контроль сервиса лаборатории SwissLab. Мы благодарим за сделанный выбор и будем рады, если вы поможете улучшить качество нашего сервиса!\n🙋 Наш оператор свяжется с вами при необходимости!')
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Ответить", callback_data='Q' + str(message.chat.id))
            markup.add(item1)
            
            for id_p in all_ids_arr:
                checkBlockedPeople(message, markup, id_p)

            oper_id = '0'
            database.insert_new_feedback_data(oper_id,  str(message.chat.id), txt, bot)
        else:
            if feedback_user != '📞 telefon' and feedback_user != '💽 Yozishmalar bazasi' and feedback_user !='🏠 manzillari' and feedback_user !='🌐 Biz ijtimoiy tarmoqlarda' and feedback_user !='🙋 Operator' and feedback_user != "☎️ O'sha.  qo'llab-quvvatlash" and feedback_user != '✍️ Direktorga yozing' and feedback_user !='📝 buyurtma yaratish' and feedback_user !='❗️ Shikoyat qoldiring' and feedback_user !='% Chegirma oling' and feedback_user !="®FAQ Ko'rsatma" and feedback_user != 'stop':
                if feedback_user == None: feedback_user = 'Пользователь отправил нечитаемый объект'
                feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})

                txt = "--------ЖАЛОБА--------\n" + "id: " + str(message.chat.id) + "\nИмя: " + feed_back[str(message.chat.id)]["Name"] + "\nЯзык: " + \
                    account_settings[str(message.chat.id)].language + "\nПричина: " + feed_back[str(message.chat.id)]["Reason"] + "\nМесто: " + \
                    feed_back[str(message.chat.id)]["Place"] + "\nДата: " + feed_back[str(message.chat.id)]["Date"] + "\nКонфликт: " + feedback_user + "\n---------------------"

                bot.send_message(message.chat.id, '➕ Laboratoriya xizmatini nazorat qilish SwissLab. Biz tanlaganingiz uchun tashakkur va xizmatimiz sifatini yaxshilashga yordam bersangiz xursand bolamiz!\n🙋 Agar kerak bolsa, bizning operatorimiz sizga murojaat qiladi!')
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Ответить", callback_data='Q' + str(message.chat.id))
                markup.add(item1)

                for id_p in all_ids_arr:
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
        account_settings[str(message.chat.id)].tags = []
        mess = ""
        
        openfileforRead('w+')
        openfileforRead('r')

    account_settings[str(message.chat.id)].tags.append(tags)
    
    openfileforRead('w+')
    openfileforRead('r')

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
        account_settings[str(message.chat.id)].tags = []
        mess = ""

        openfileforRead('w+')
        openfileforRead('r')

    account_settings[str(message.chat.id)].tags.append(tags)
    
    openfileforRead('w+')
    openfileforRead('r')

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
    if account_settings[str(message.chat.id)].language == "Русский":
        bot.send_photo(message.chat.id, contents, caption='💳 Ваша карта')
    else:
        bot.send_photo(message.chat.id, contents, caption='💳 Sizning kartangiz')
    os.remove('newAcc.png')


def refAdd(message):
    global account_settings
    ref_n = message.text
    openfileforRead('r')
    ch_ref = "none"
    for k in account_settings.keys():
        if k == ref_n:
            ch_ref = "yes"
            break
    if ch_ref == "yes":
        if int(account_settings[ref_n].ref) < 10:
            account_settings[ref_n].ref = str(int(account_settings[ref_n].ref) + 1)
            
            openfileforRead('w+')
            openfileforRead('r')
            
            if account_settings[str(message.chat.id)].language == "Русский":
                bot.send_message(message.chat.id, "✅ Спасибо за активацию!")
                bot.send_message(ref_n, "✅ Новый пользователь активировал реферальный код!")
                keyboardRefMaker(message, 0)
            else:
                bot.send_message(message.chat.id, "✅ Faollashtirish uchun rahmat!")
                bot.send_message(ref_n, "✅ Yangi foydalanuvchi tavsiya kodini faollashtirdi!")
                keyboardRefMaker(message, 1)
        else:
            if account_settings[str(message.chat.id)].language == "Русский":
                bot.send_message(message.chat.id, "⚠️ Активации кода закончены")
                keyboardRefMaker(message, 0)
            else:
                bot.send_message(message.chat.id, "⚠️ Kodni faollashtirish tugadi")
                keyboardRefMaker(message, 1)
    elif ref_n == "stop":
        if account_settings[str(message.chat.id)].language == "Русский":
            keyboardRefMaker(message, 0)
        else:
            keyboardRefMaker(message, 1)
    else:
        if account_settings[str(message.chat.id)].language == "Русский":
            send = bot.send_message(message.chat.id, '❔ Ваш код не найден, поробуйте ещё раз или напишите - stop')
        else:
            send = bot.send_message(message.chat.id, '❔ Sizning kodingiz topilmadi, yana porobuyte yoki yozing - stop')
        bot.register_next_step_handler(send, refAdd)


def userSebdText(message):
    global account_settings
    if message.text != 'stop':
        if account_settings[account_settings[str(message.chat.id)].feedback_st].language == 'Русский':
            oper_ans = 'Ответ оператора #' + account_settings[str(message.chat.id)].feedback_st + ' на вашу жалобу!👇'
            bot.send_message(account_settings[str(message.chat.id)]["feedback_st"], oper_ans)
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
        account_settings[account_settings[str(message.chat.id)].feedback_st].feedback_st = 'close'
        account_settings[str(message.chat.id)].feedback_st = 'close'
        
        openfileforRead('w+')
        openfileforRead('r')

    else: bot.send_message(message.chat.id, 'Операция отменена!')



def inlineMessages(call, text1, text2, callback_data1, callback_data2, markup_text):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(text=text1, callback_data=callback_data1)
    item2 = types.InlineKeyboardButton(text=text2, callback_data=callback_data2)
    markup.add(item1, item2)
    bot.send_message(call.message.chat.id, markup_text.format(call.message.chat, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global new_acc_id
    global account_settings
    global mess
    try:
        if call.data == 'Русский':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            account_settings[new_acc_id].language = "Русский"
            new_acc_id = ""
            
            openfileforRead('w+')
            openfileforRead('r')

            start_txt = openfileforRead(None, path_first_lang)

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Согласен", callback_data='Согласен')
            item2 = types.InlineKeyboardButton("Отказываюсь", callback_data='Отказываюсь')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, start_txt.format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'Отказываюсь':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Вы отказались от обработки персональных данных\n♻️ Для перезапуска бота нажмите /start")
        elif call.data == 'Согласен':
            inlineMessages(call, text1='Да', text2='Нет', callback_data1='Да', callback_data2='Нет' , markup_text='♻️ У вас есть реферальная ссылка?')

        elif call.data == 'Нет':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            keyboardRefMaker(call.message, 0)
        elif call.data == 'Да':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Отправьте код')
            bot.register_next_step_handler(send, refAdd)

        elif call.data == 'Ozbek':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            account_settings[new_acc_id].language = "Ozbek"
            new_acc_id = ""
            
            openfileforRead('w+')
            openfileforRead('r')

            start_txt = openfileforRead(None, path_second_lang)

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("ROZIMAN", callback_data='Agree')
            item2 = types.InlineKeyboardButton("Qo'shilmayman", callback_data='Disagree')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, start_txt.format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'Disagree':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Siz shaxsiy ma'lumotlarni qayta ishlash uchun rad qilgan\n♻️ Botni qayta ishga tushirish uchun bosing /start")
        elif call.data == 'Agree':
            inlineMessages(call, text1='Ha', text2="Yo'q", callback_data1='Yes', callback_data2='No' , markup_text="♻️ Yo'naltiruvchi havola bormi?")
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
        elif call.data == 'Write a feedback':
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
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangStart', callback_data2='OzbekLangStart' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangStart':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_first_lang)
        elif call.data == 'OzbekLangStart':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_second_lang)

        elif call.data == 'FAQ текст':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangFAQ', callback_data2='OzbekLangFAQ' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_FAQ_label)
        elif call.data == 'OzbekLangFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_FAQ_label)

        elif call.data == 'Текст оператора':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangOper', callback_data2='OzbekLangOper' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangOper':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_oper_label)
        elif call.data == 'OzbekLangOper':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_oper_label)

        elif call.data == 'Текст телефона':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangTele', callback_data2='OzbekLangTele' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangTele':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_telephone_num)
        elif call.data == 'OzbekLangTele':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_telephone_num)

        elif call.data == 'Текст адресса':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangAdress', callback_data2='OzbekLangAdress' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangAdress':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_address_label)
        elif call.data == 'OzbekLangAdress':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_address_label)

        elif call.data == 'Текст создания заказа':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangOrder', callback_data2='OzbekLangOrder' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangOrder':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_order_label)
        elif call.data == 'OzbekLangOrder':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_order_label)

        elif call.data == 'Текст отзыва':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangRecv', callback_data2='OzbekLangRecv' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangRecv':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_recv_label)
        elif call.data == 'OzbekLangRecv':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_recv_label)

        elif call.data == 'Текст скидки':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangDisc', callback_data2='OzbekLangDisc' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangDisc':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_discount_label)
        elif call.data == 'OzbekLangDisc':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_discount_label)

        elif call.data == 'Текст социальные сети':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangSocial', callback_data2='OzbekLangSocial' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangSocial':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_social_web)
        elif call.data == 'OzbekLangSocial':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_social_web)

        elif call.data == 'Текст инструкции оператора':
            inlineMessages(call, text1='Русский', text2='Ozbek', callback_data1='РусскийLangOperFAQ', callback_data2='OzbekLangOperFAQ' , markup_text='Выберите язык блока')
        elif call.data == 'РусскийLangOperFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewText, path_FAQoper_label)
        elif call.data == 'OzbekLangOperFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewText, path_sec_FAQoper_label)

        elif call.data == '👍':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if account_settings[str(call.message.chat.id)].language == "Русский":
                bot.send_message(call.message.chat.id, 'Спасибо за оценку!')
            else: bot.send_message(call.message.chat.id, 'Baholash uchun rahmat!')
        elif call.data == '👎':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if account_settings[str(call.message.chat.id)].language == "Русский":
                bot.send_message(call.message.chat.id, 'Спасибо за оценку!')
            else: bot.send_message(call.message.chat.id, 'Baholash uchun rahmat!')

        elif call.data[0] == 'Q':
            if account_settings[call.data[1:]].feedback_st == 'open':
                account_settings[call.data[1:]].feedback_st = 'close'
                account_settings[str(call.message.chat.id)].feedback_st = call.data[1:]
                
                openfileforRead('w+')
                openfileforRead('r')

                send = bot.send_message(call.message.chat.id, "➕ Введите текст для ответа пользователю")
                bot.register_next_step_handler(send, userSebdText)
            else:
                bot.send_message(call.message.chat.id, "Оператор уже ответил этому пользователю!\nДля отмены повторного ответа напишите stop")
                account_settings[call.data[1:]].feedback_st = 'close'
                account_settings[str(call.message.chat.id)].feedback_st = call.data[1:]
                
                openfileforRead('w+')
                openfileforRead('r')

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
                        account_settings[str(call.message.chat.id)].conversation = 'open'
                        account_settings[k].tags.append(str(call.message.chat.id))
                        account_settings[k].tags.append("0")
                        account_settings[k].conversation = 'open'
                        
                        account_settings[k].timer_conv = int(time.time())

                        openfileforRead('w+')
                        openfileforRead('r')

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
                        account_settings[str(call.message.chat.id)].conversation = 'open'
                        account_settings[str(call.data)].tags.append(str(call.message.chat.id))
                        account_settings[str(call.data)].tags.append("0")
                        account_settings[str(call.data)].conversation = 'open'
                        account_settings[str(call.data)].timer_conv = int(time.time())
                        
                        openfileforRead('w+')
                        openfileforRead('r')

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
                            account_settings[str(call.message.chat.id)].conversation = 'close'
                            account_settings[str(call.data)].tags = []
                            account_settings[str(call.message.chat.id)].tags = []
                            bot.send_message(call.message.chat.id, 'Пользователь выключил бота!')
                            
                            openfileforRead('w+')
                            openfileforRead('r')
                    else:
                        bot.send_message(str(call.message.chat.id), "Другой оператор отвечает на заявку!")
            else:
                bot.send_message(call.message.chat.id, "Закончите старый диалог, чтобы начать новый!")


    except Exception as e:
        print("Error in the 'call' part!", repr(e))
        for id_er in label_change_ids_arr:
            bot.send_message(int(id_er), "Error in the 'call' part!\n\n"+ traceback.format_exc())

if __name__ == '__main__':
    start_process()
    try:
        bot.polling(none_stop=True)
    except Exception as _:
        for id_er in label_change_ids_arr:
            bot.send_message(int(id_er), "Program error!\n\n"+ traceback.format_exc())
