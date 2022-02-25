# Main libraries
import schedule, telebot, time, io, os, traceback
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Process
from telebot import types

# Project files
import config, database, classes, path, variables, utility, debug

account = database.get_accounts_data()

def openfileforRead(action = None, file = None, text = '') -> str:
    return text.join([i for i in io.open(file, encoding='utf-8')])

def langCheck(account, message = None, id = None) -> bool:
    """
    This def returns True if the language is Russian.
    """
    return True if account[str(message.chat.id) if id == None else str(id)].language == "Русский" else False

def saveNewText(message, file) -> None:
    bot.send_message(message.chat.id, variables.changes_message[utility.saveText(message.text, file, 'w')])

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
    return True if person_id in [id for id in action] else False

def markupMaker(mode, button) -> types.ReplyKeyboardMarkup():
    markup =  types.ReplyKeyboardMarkup(resize_keyboard=True)
    pin    = [types.KeyboardButton(tag) for tag in button.keys() if mode in button[tag]]

    if 'user' != mode != 'redirect': markup.add(*pin) 
    elif         mode != 'redirect': markup.row(*pin[0:2], pin[3]).row(*pin[5:6], pin[8]).row(pin[10]).row(pin[2:8:5]).row(pin[4:10:5])
    else                           : markup.row(pin[0:2]).row(pin[2:4], pin[4]).row(pin[5:7])
    return markup

bot = telebot.TeleBot(config.TOKEN)

class P_schedule:
    """
    This class reposts messages from the telegram channel.
    """

    def start_schedule():
        schedule.every(30).seconds.do(P_schedule.send_post)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def send_post():
        c_ex = 0
        message_id = database.dbMessageId(action = 'take_id')[0][0]
        account = database.get_accounts_data()
        for account in account.keys():
            try:
                bot.forward_message(int(account), variables.CHANNEL_ID, message_id)
                time.sleep(1)
            except Exception as _:
                c_ex+=1
                continue
            try:
                if (int(time.time()) - account[account].timer_conv) > 900 and account[account].conversation == 'open':
                    stopConversation(message = None, lang = 0 if langCheck(account, message = None, person_id = account) else 1, pers_id = account)
            except Exception as _: pass
        if c_ex == len(account): c_ex = 0
        else:
            try:
                bot.forward_message(281321076, variables.CHANNEL_ID, message_id)
                database.dbMessageId(action = 'save_id', message_id = message_id + 1)
            except Exception as error:
                print(f"Error pushing news!\n\n{repr(error)}")
                for id_er in variables.label_change_ids_arr:
                    bot.send_message(int(id_er), f"Error pushing news!\n\n{repr(error)}")


@bot.message_handler(commands=['start'])
def welcome(message):
    global account
    
    account = database.get_accounts_data()

    new_account = [str(message.chat.id)]
    
    for account in account.keys():
        if account[account].telegram_id == new_account[0]:
            if account[account].language == "Русский":
                if account[account].personal_data == "YES":
                    bot.send_message(message.chat.id,"🔱Вы уже зарегистрированы в системе!")
                    keyboardRefMaker(message = message, lang = 0)
                elif account[account].personal_data == "NO":
                    inlineMessages(markup_text = openfileforRead(None, path.first_lang), message = message, 
                                   markup_arr = [["Согласен"   , "Согласен"   ], 
                                                 ["Отказываюсь", "Отказываюсь"]], action = False
                                  )
            elif account[account].language == "Ozbek":
                if account[account].personal_data == "YES":
                    bot.send_message(message.chat.id,"🔱Siz allaqachon ro'yxatdan o'tgansiz!")
                    keyboardRefMaker(message = message, lang = 1)
                elif account[account].personal_data == "NO":
                    inlineMessages(markup_text = openfileforRead(None, path.second_lang), message = message,
                                   markup_arr = [["ROZIMAN"      , "Agree"   ], 
                                                 ["Qo'shilmayman", "Disagree"]], action = False
                                  )
            else:
                inlineMessages(markup_text = "🔱Choose language", message = message, 
                               markup_arr = [["Русский", "Русский"], ["Ozbek", "Ozbek"]], action = False)
            break
    else:
        new_account += [str(message.chat.username), str(message.chat.first_name), [], "close", "0", [], "0", "NO", None, 'close', 0]
        account = classes.Account(new_account)
        database.insert_account_data(account)
        account[account.telegram_id] = account
        inlineMessages(markup_text = "🔱Choose language", message = message, 
                       markup_arr = [["Русский", "Русский"], ["Ozbek", "Ozbek"]], action = False)

@bot.message_handler(commands=['changeLabel'])
def adderNewLabel(message):
    if checkOperId(person_id = str(message.chat.id), action = variables.label_change_ids_arr):
        inlineMessages(markup_text = "Какой блок надо отредактировать?", message = message, 
                       markup_arr = variables.markup_change_label_arr, action = False)

def sendReqtoOper(which_oper, oper_send_text, markup):
    for oper_id in variables.action_oper_select[which_oper]:
        bot.send_message(int(oper_id), oper_send_text, reply_markup=markup)

def operKeyboardMaker(message, which_oper, lang):
    global account
    account[str(message.chat.id)].conversation = 'mid'
    variables.message_ids_dict[str(message.chat.id)] = message

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(f"{variables.emj.EMJ_BACK_ARROW} Отклонить вызов оператора" 
                  if lang == 0 else f"{variables.emj.EMJ_BACK_ARROW} Operator chaqiruvini rad etish"), 
               types.KeyboardButton(f"{variables.emj.EMJ_QUESTION} Инструкция" 
                  if lang == 0 else f"{variables.emj.EMJ_QUESTION} Ko'rsatma"))

    bot.send_message(message.chat.id, f"{variables.emj.EMJ_RAISING_HAND} Включён режим переписки с оператором" 
                    if lang == 0 else f"{variables.emj.EMJ_RAISING_HAND} Operator bilan yozishmalar rejimi yoqilgan", reply_markup=markup)

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Принять", callback_data=str(message.chat.id)))
    
    database.insert_new_data(str(message.chat.id), '0')

    sendReqtoOper(which_oper = which_oper, oper_send_text = (f"-------Запрос переписки!-------\n"
                                                             f"id: {message.chat.id} \n"
                                                             f"Имя: {message.chat.first_name} \n"
                                                             f"Фамилия: {message.chat.last_name} \n"
                                                             f"Username: @ {message.chat.username} \n"
                                                             f"Язык: Русский\n----------------------------"), markup = markup)

def dbDateSortEnter(message, action):
    nextStepWait(person_id = message.chat.id, text = variables.db_conv_message['date'], func = dbSortEnter, args = [action])
def dbSortEnter(message, action):
    date_text = database.getDataFromDB(date_start = message.text, action = action)
    if date_text: 
        bot.send_message(message.chat.id, variables.db_conv_message['no_date'])
    else:
        bot.send_message(message.chat.id, date_text)
        nextStepWait(person_id = message.chat.id, text = variables.db_conv_message['name'], func = dbIdSortEnter, args = [action])
def dbIdSortEnter(message, action):
    id_text = database.getTextFromDB(id_text = message.text, action = action)
    bot.send_message(message.chat.id, id_text if id_text != 0 else 'Такого номера нет в базе!')
    return

def pushingLabelFromFile(message, path, path_sec):
    bot.send_message(message.chat.id, openfileforRead(None, path if langCheck(message) 
                                                                 else path_sec).format(message.chat, bot.get_me()),parse_mode='html')

def operInit(message, action, set_act, id_check, deactivation=None):
    if checkOperId(person_id = str(message.chat.id), action = action): bot.send_message(message.chat.id, "Вы оператор!")
    else: operKeyboardMaker(message = message, which_oper = set_act, lang = 0 if langCheck(message) else 1)
        
def redirectInit(message, action):
    global account

    bot.send_message(str(message.chat.id), action)
    if len(account[str(message.chat.id)].tags) != 0:

        bot.send_message(str(account[str(message.chat.id)].tags[0]), action)
        
        database.change_account_data(account = account[account[str(message.chat.id)].tags[0]], parametr = 'conversation', data = 'close')
        database.change_account_data(account = account[account[str(message.chat.id)].tags[0]], parametr = 'tags', data = [])        
        account = database.get_accounts_data()

        keyboardRefMaker(message = message, lang = 0 if langCheck(message) else 1, pers_id = account[str(message.chat.id)].tags[0])

    keyboardRefMaker(message = message, lang = 0)
    inlineMessages(markup_text = 'Оцените работу оператора!' if langCheck(message) else 'Operator ishini baholang!', 
                   person_id = account[str(message.chat.id)].tags[0] if checkOperId(person_id = str(message.chat.id), 
                   action = variables.all_ids_arr) else str(message.chat.id), markup_arr = [["👍", "👍"], ["👎", "👎"]], action = False)

   
def stopConversation(message, lang, pers_id=None, action = None):
    global account
    person_id = pers_id if pers_id != None else str(message.chat.id)
    push_text = f"{variables.emj.EMJ_EXCLAMATION} Завершение диалога" if lang == 0 or lang == 'Русский' else f"{variables.emj.EMJ_EXCLAMATION} Muloqotni yakunlash"
    bot.send_message(person_id, push_text)
    if len(account[person_id].tags) != 0:
        bot.send_message(str(account[person_id].tags[0]), push_text)
            
        database.change_account_data(account = account[account[person_id].tags[0]], parametr = 'conversation', data = 'close')
        database.change_account_data(account = account[account[person_id].tags[0]], parametr = 'tags', data = [])        
        account = database.get_accounts_data()

        keyboardRefMaker(None, 0 if account[account[person_id].tags[0]].language == "Русский" else 1, account[person_id].tags[0])
    keyboardRefMaker(None, lang, person_id)
    
    if not checkOperId(person_id = person_id, action = variables.all_ids_arr):
        user_id = account[person_id].tags[0] if checkOperId(person_id = person_id, action = variables.all_ids_arr) and action == None else person_id
        inlineMessages(markup_text = 'Оцените работу оператора!' if langCheck(person_id = user_id) else 'Operator ishini baholang!', 
                       person_id = user_id, markup_arr = [['👍', '👍'], ['👎', '👎']], action = False)
            
    database.change_account_data(account = account[person_id], parametr = 'conversation', data = 'close')
    database.change_account_data(account = account[person_id], parametr = 'tags', data = [])        
    account = database.get_accounts_data()
            
    database.closerDataBase(person_id, bot)

def closeConversation(message):
    global account
            
    database.change_account_data(account = account[str(message.chat.id)], parametr = 'conversation', data = 'close')
    database.change_account_data(account = account[str(message.chat.id)], parametr = 'tags', data = [])        
    account = database.get_accounts_data()
            
    database.closerDataBase(str(message.chat.id), bot)


def setCollectionKeyboard(message, person_id, show_text = 'Выберите необходимый мед офис'):
    bot.send_message(person_id, show_text, reply_markup = markupMaker(action = 'office', button_text = variables.office_markup_dict))

def selectOffice(message, person_id, step, push_text = '', data = ''):
    if checkOperId(person_id = person_id, action = variables.collection_oper_ids_arr):
        if variables.show_text_dict[step]:
            database.dbCollection(message = message, person_id = person_id, step = step - 1, database_push_data = message.text)
            nextStepWait(person_id = person_id, text = variables.show_text_dict[step], func = selectOffice, args = [person_id, step + 1])
        else:
            database.dbCollection(message = message, person_id = person_id, step = step - 1, database_push_data = message.text)
            for line, row in zip(variables.add_text_dict, database.dbCollection(message = message, person_id = person_id, step = step, database_push_data = 'admin')[-1]):
                data += f"{line} {row}\n"
            bot.send_message(person_id, data)
            inlineMessages(markup_text = 'Можете отправить отчёт или изменить данные', message = message, 
                           markup_arr = [['Отправить отчёт', 'Отправить отчёт'], ['Изменить', 'Изменить']])

    elif checkOperId(person_id = person_id, action = variables.collection_cash_ids_arr):
        database.dbCollection(message = message, person_id = person_id, database_push_data = message.text, action = 'cashier_init')
        database_data = database.dbCollection(message = message, person_id = person_id, database_push_data = message.text, step = 9, action = 'show_collection_to_cashier')
        if len(database_data) > 0:
            for line, row in zip(variables.add_text_dict, database_data[-1]):
                data += f"{line} {row}\n"
            bot.send_message(person_id, data)
            inlineMessages(markup_text = 'Можете подтвердить или изменить данные', message = message, markup_arr = [['Подтвердить', 'Подтвердить'], ['Изменить', 'Изменить']])
        else:
            bot.send_message(person_id, 'Данных по этому офису нет!')


@bot.message_handler(content_types=['text', 'photo'])
def lol(message):
    global account
    account = database.get_accounts_data()
    
    if message.chat.type == 'private':
        if message.text in variables.message_text_dict.keys():
            if   variables.message_text_dict[message.text][0] == 'office': 
                selectOffice(message, str(message.chat.id), variables.STEP_FIRST)
            elif variables.message_text_dict[message.text][0] == 'text_show': 
                pushingLabelFromFile(message, variables.message_text_dict[message.text][1], variables.message_text_dict[message.text][2])
            elif variables.message_text_dict[message.text][0] == 'oper_show': 
                operInit(message, variables.message_text_dict[message.text][1], variables.message_text_dict[message.text][2], str(message.chat.id))
            elif variables.message_text_dict[message.text][0] == 'oper_close': 
                stopConversation(message, variables.message_text_dict[message.text][1])
            elif variables.message_text_dict[message.text][0] == 'redirect'  :
                redirectInit(message, f"{variables.emj.EMJ_EXCLAMATION} Общение завершено, перенаправление {variables.message_text_dict[message.text][1]}")
                operInit(variables.message_ids_dict[account[str(message.chat.id)].tags[0]], variables.message_text_dict[message.text][2], 
                         variables.message_text_dict[message.text][3], closeConversation(message))
        elif message.text == f'{variables.emj.EMJ_BACK_ARROW} Назад': 
            keyboardRefMaker(message = message, lang = account[str(message.chat.id)].language)
        elif message.text == f'{variables.emj.EMJ_EXCLAMATION} Оставить жалобу' or message.text == f'{variables.emj.EMJ_EXCLAMATION} Shikoyat qoldiring':
            if checkOperId(person_id = str(message.chat.id), action = variables.feedback_oper_ids_arr): dbDateSortEnter(message = message, action = 'feedback_tb')
            else:
                account[str(message.chat.id)].feedback_st = 'open'
                inlineMessages(markup_text = openfileforRead(None, path.recv_label if langCheck(message) else path.sec_recv_label), message = message, 
                               markup_arr = [["Написать жалобу", "Написать жалобу"] if langCheck(message) else ["Shikoyat yozing", "Shikoyat yozing"]], action = False)
        elif message.text == f"{variables.emj.EMJ_MONEY_BAG} Инкассация": 
            setCollectionKeyboard(message = message, person_id = str(message.chat.id))
        elif message.text == f'{variables.emj.EMJ_DISK} БД переписок' or message.text == f'{variables.emj.EMJ_DISK} Yozishmalar bazasi':
            if checkOperId(person_id = str(message.chat.id), action = variables.all_ids_arr): dbDateSortEnter(message = message, action = 'message_tb')
            else: bot.send_message(message.chat.id, 'У вас нет прав для чтения базы!' if langCheck(message) else "Sizda bazani o'qish huquqi yo'q!")
        elif message.text == '% Получить скидку' or message.text == '% Chegirma oling':
            if account[str(message.chat.id)].discount == "0" and account[str(message.chat.id)].ref == "0":
                bot.send_message(message.chat.id, openfileforRead(None, path.discount_label if langCheck(message) else path.sec_discount_label) + ("\nВаш реферальный код: " if langCheck(message) else  f"\nSizning tavsiyangiz kodi: ") + str(message.chat.id).format(message.chat, bot.get_me()),parse_mode='html')
            elif account[str(message.chat.id)].ref == "10":
                database.change_account_data(account = account[str(message.chat.id)], parametr = 'discount', data = '10')       
                account = database.get_accounts_data()
                bot.send_message(message.chat.id, f"{variables.emj.EMJ_DONE} У вас максимальная скидка!" if langCheck(message) 
                                             else f"{variables.emj.EMJ_DONE} Siz maksimal chegirma bor!")
                picPNGmaker(message)
            else:
                if account[str(message.chat.id)].discount == "10":
                    bot.send_message(message.chat.id, f"{variables.emj.EMJ_DONE} У вас максимальная скидка!" if langCheck(message) 
                                                 else f"{variables.emj.EMJ_DONE} Siz maksimal chegirma bor!")
                    picPNGmaker(message)
                else:
                    bot.send_message(message.chat.id, f"{variables.emj.EMJ_CROSS} Ваши друзья ещё не активировали бота!\n"
                                                      f"{variables.emj.EMJ_CROSS} Всего активаций {account[str(message.chat.id)].ref} из 10" if langCheck(message) 
                                                 else f"{variables.emj.EMJ_CROSS} Sizning do'stlaringiz hali botni faollashtirmagan!\n"
                                                      f"{variables.emj.EMJ_CROSS} Jami aktivatsiyalar {account[str(message.chat.id)].ref} dan 10")
                    picPNGmaker(message)
        elif message.text == f"{variables.emj.EMJ_EXCLAMATION} Жалоба":
            redirectInit(message, f"{variables.emj.EMJ_EXCLAMATION} Общение с оператором завершено, перенаправление в раздел жалоб")
            account[account[str(message.chat.id)].tags[0]].feedback_st = 'open'
            inlineMessages(markup_text = openfileforRead(None, path.recv_label if langCheck(message) else path.sec_recv_label), 
                           person_id = account[str(message.chat.id)].tags[0], markup_arr = [ ["Написать жалобу", "Написать жалобу"] if langCheck(message) 
                                                                                                 else ["Shikoyat yozing", "Shikoyat yozing"] ], action = False)
            closeConversation(message)        
        else:
            if account[str(message.chat.id)].conversation == 'open':
                if checkOperId(person_id = str(message.chat.id), action = variables.all_ids_arr):
                    database.change_account_data(account = account[account[str(message.chat.id)].tags[0]], parametr = 'timer_conv', data = int(time.time()))
                    sm_id = 'Operator: '
                else:
                    database.change_account_data(account = account[str(message.chat.id)], parametr = 'timer_conv', data = int(time.time()))
                    sm_id = 'User: '
      
                account = database.get_accounts_data()

                if message.text != None:
                    sm_id = f'{sm_id}{message.text}\n'
                    bot.send_message(account[str(message.chat.id)].tags[0], message.text)
                elif message.caption != None:
                    sm_id = f'{sm_id}{message.caption}\n'
                    bot.send_message(account[str(message.chat.id)].tags[0], message.caption)
                if message.photo != None:
                    sm_id = f'{sm_id}PHOTO\n'
                    bot.send_photo(account[str(message.chat.id)].tags[0], bot.download_file(bot.get_file(message.photo[-1].file_id).file_path))
                database.insert_text_to_data(sm_id, str(message.chat.id), bot)

def picPNGmaker(message):
    img = Image.open('bonus_card/lab.png')
    ImageDraw.Draw(img).text((150,280), f"{message.chat.first_name} {'' if message.chat.last_name == None else message.chat.last_name}", fill = 'orange', font = ImageFont.truetype('Arial.ttf', size = 45))
    img.save('newAcc.png')
    bot.send_photo(message.chat.id, open('newAcc.png', 'rb').read(), caption = '💳 Ваша карта' if langCheck(message) else '💳 Sizning kartangiz')
    os.remove('newAcc.png')

def keyboardRefMaker(message, lang, pers_id=None):
    global account
    person_id = pers_id if pers_id != None else str(message.chat.id)
    markup = markupMaker(action = 'admin' 
                         if checkOperId(person_id = person_id, action = variables.collection_cash_ids_arr + variables.collection_oper_ids_arr) else 'oper' 
                         if checkOperId(person_id = person_id, action = variables.all_ids_arr) else 'user', button_text = variables.buttons_ru_text 
                         if lang or lang == 'Русский' else variables.buttons_uz_text
                        )
    bot.send_message(person_id, openfileforRead(None, path.FAQ_label if lang == 0 or lang == 'Русский' else path.sec_FAQ_label) 
                                if not checkOperId(person_id, variables.all_ids_arr) else 'Открыта клавиатура оператора!', parse_mode='html', reply_markup=markup)
    
    if person_id != pers_id:        
        account = database.get_accounts_data()
        database.change_account_data(account = account[str(message.chat.id)], parametr = 'personal_data', data = 'YES')
        account = database.get_accounts_data()


def checkBlockedPeople(markup, pers_id, txt):
    try: bot.send_message(pers_id, txt, reply_markup=markup)
    except Exception as error:
        for id_er in variables.label_change_ids_arr:
            bot.send_message(int(id_er), f"User {pers_id} blocked!\n\n{repr(error)}")


def fdbackName(message, lang):
    global account
    name_user = message.text
    if name_user != 'stop':
        if name_user is None: name_user = 'Пользователь отправил нечитаемый объект'

        variables.feed_back[str(message.chat.id)] = {
                                                     "Name" : name_user, 
                                                     "Username" : str(message.chat.username), 
                                                     "Language" : account[str(message.chat.id)].language
                                                    }
        nextStepWait(person_id = message.chat.id, text = f'{variables.emj.EMJ_PLUS} Введите ваш номер телефона' if lang == 0 
                                                    else f'{variables.emj.EMJ_PLUS} Telefon raqamingizni kiriting', func = fdbackTele, args = [lang])
    else:
        bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Операция отменена')
def fdbackTele(message, lang):
    tele_num = message.text
    if tele_num.isdigit():

        variables.feed_back[str(message.chat.id)].update({
                              'Telephone number' : tele_num if tele_num != None else 'Пользователь отправил нечитаемый объект'
                                                         })

        if lang: bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Жалоба составляется в четыре этапа:\n'
                                                    '1) Причина жалобы и номер заявки\n'
                                                    '2) Обозначение филиала/места, где произошёл инцидент\n'
                                                    '3) Дата инцидента\n'
                                                    '4) Имя или опишите оппонента, с которым произошёл конфликт\n'
                                                   f'{variables.emj.EMJ_CROSS} Для отмены операции напишите stop')
        else:    bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Shikoyat tort bosqichda tuziladi:\n'
                                                    '1) Shikoyat sababi\n'
                                                    '2) Hodisa sodir bolgan filial/joyni belgilash\n'
                                                    '3) Hodisa sanasi\n'
                                                    '4) Mojaro yuz bergan raqibning nomi yoki tarifi\n'
                                                   f'{variables.emj.EMJ_CROSS} Operatsiyani bekor qilish uchun yozing stop')
                                                                       
        nextStepWait(person_id = message.chat.id, text = f'{variables.emj.EMJ_PLUS} Напишите причину жалобы и номер заявки' 
                                       if lang == 0 else f'{variables.emj.EMJ_PLUS} Shikoyat sababini va ariza raqamini yozing', func = fdbackReason, args = [lang])
    elif tele_num == 'stop': bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Операция отменена' 
                                             if lang == 0 else f'{variables.emj.EMJ_PLUS} Amal bekor qilindi')
    else: nextStepWait(person_id = message.chat.id, text = f'{variables.emj.EMJ_PLUS} Введите номер телефона в формате 998999999999 или напишите stop' 
                                         if lang == 0 else f'{variables.emj.EMJ_PLUS} Telefon raqamingizni formatda kiriting 9997777777777 yoki yozing stop', func = fdbackTele, args = [lang])
def fdbackReason(message, lang):
    reason_send = message.text
    if reason_send != 'stop':
        if reason_send == None: reason_send = 'Пользователь отправил нечитаемый объект'
        variables.feed_back[str(message.chat.id)].update({"Reason" : reason_send})
        
        nextStepWait(person_id = message.chat.id, text = f'{variables.emj.EMJ_PLUS} Напишите филиал/место, где произошёл инцидент' 
                                       if lang == 0 else f'{variables.emj.EMJ_PLUS} Hodisa sodir bolgan filial/joyni yozing', func = fdbackPlace, args = [lang])
    else:
        bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Операция отменена' 
                        if lang == 0 else f'{variables.emj.EMJ_PLUS} Amal bekor qilindi')  
def fdbackPlace(message, lang):
    place_send = message.text
    if place_send != 'stop':
        if place_send == None: place_send = 'Пользователь отправил нечитаемый объект'
        variables.feed_back[str(message.chat.id)].update({"Place" : place_send})
        nextStepWait(person_id = message.chat.id, text = f'{variables.emj.EMJ_PLUS} Напишите дату инцидента' 
                                       if lang == 0 else f'{variables.emj.EMJ_PLUS} Hodisa tarixini yozing', func = fdbackDate, args = [lang])
    else: bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Операция отменена' if lang == 0 else f'{variables.emj.EMJ_PLUS} Amal bekor qilindi')
def fdbackDate(message, lang):
    date_send = message.text
    if date_send != 'stop':
        variables.feed_back[str(message.chat.id)].update({"Date" : date_send if date_send != None else 'Пользователь отправил нечитаемый объект'})
        nextStepWait(person_id = message.chat.id, text = f'{variables.emj.EMJ_PLUS} Напишите имя или опишите оппонента, с которым произошёл конфликт' 
                                       if lang == 0 else f'{variables.emj.EMJ_PLUS} Ismni yozing yoki ziddiyatga duch kelgan raqibni tariflang', func = fdBack_fill, args = [lang])
    else: bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Операция отменена' 
                          if lang == 0 else f'{variables.emj.EMJ_PLUS} Amal bekor qilindi')
def fdBack_fill(message, lang):

    feedback_user = message.text

    if lang:
        if (feedback_user not in [
                    f'{variables.emj.EMJ_WRITING_HAND} Написать директору' ,  f'{variables.emj.EMJ_OLD_TELEPHONE} Тех. поддержка',
                    f'{variables.emj.EMJ_EXCLAMATION}️ Оставить жалобу'     ,  f'{variables.emj.EMJ_NOTE} Создать заказ'          ,
                    f'{variables.emj.EMJ_RAISING_HAND} Оператор'           ,  f'{variables.emj.EMJ_DISK} БД переписок'           ,
                    f'{variables.emj.EMJ_INFO} FAQ Инструкция'             ,  f'{variables.emj.EMJ_GLOBE} Соц. сети'             ,
                    f'{variables.emj.EMJ_TELEPHONE} Телефон'               ,  f'{variables.emj.EMJ_HOUSE} Адреса'                ,
                     '% Получить скидку'                                   ,  'stop'                                              ]
            ):
            
            if feedback_user is None: feedback_user = 'Пользователь отправил нечитаемый объект'

            variables.feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})

            txt = (
                  f"--------ЖАЛОБА--------\n"
                  f"id: {str(message.chat.id)}\n"
                  f"Имя: {variables.feed_back[str(message.chat.id)]['Name']}\n"
                  f"Язык: {account[str(message.chat.id)].language}\n"
                  f"Причина: {variables.feed_back[str(message.chat.id)]['Reason']}\n"
                  f"Место: {variables.feed_back[str(message.chat.id)]['Place']}\n"
                  f"Дата: {variables.feed_back[str(message.chat.id)]['Date']}\n"
                  f"Конфликт: {feedback_user}\n---------------------"
            )

            bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Контроль сервиса лаборатории SwissLab. Мы благодарим за'
                                               ' сделанный выбор и будем рады, если вы поможете улучшить качество нашего сервиса!\n'
                                              f'{variables.emj.EMJ_RAISING_HAND} Наш оператор свяжется с вами при необходимости!')

            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("Ответить", callback_data = f"Q{str(message.chat.id)}"))
            
            for id_p in variables.all_ids_arr:
                checkBlockedPeople(markup = markup, pers_id = id_p, txt = txt)

            database.insert_new_feedback_data(oper_id = '0', user_id = str(message.chat.id), txt = txt, bot = bot)

        elif (
                feedback_user not in [
                    f"{variables.emj.EMJ_OLD_TELEPHONE} O'sha.  qo'llab-quvvatlash" , f'{variables.emj.EMJ_EXCLAMATION} Shikoyat qoldiring',
                    f'{variables.emj.EMJ_GLOBE} Biz ijtimoiy tarmoqlarda'           , f'{variables.emj.EMJ_DISK} Yozishmalar bazasi'       ,
                    f'{variables.emj.EMJ_WRITING_HAND} Direktorga yozing'           , f"{variables.emj.EMJ_INFO} FAQ Ko'rsatma"            ,
                    f'{variables.emj.EMJ_NOTE} buyurtma yaratish'                   , f'{variables.emj.EMJ_TELEPHONE} telefon'             ,
                    f'{variables.emj.EMJ_RAISING_HAND} Operator'                    , f'{variables.emj.EMJ_HOUSE} manzillari'              ,
                     '% Chegirma oling'                                             ,  'stop' 
                ]
             ):

                if feedback_user == None: feedback_user = 'Пользователь отправил нечитаемый объект'
                
                variables.feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})

                txt = (
                    f"--------ЖАЛОБА--------\n"
                    f"id: {str(message.chat.id)}\n"
                    f"Имя: {variables.feed_back[str(message.chat.id)]['Name']}\n"
                    f"Язык: {account[str(message.chat.id)].language}\n"
                    f"Причина: {variables.feed_back[str(message.chat.id)]['Reason']}\n"
                    f"Место: {variables.feed_back[str(message.chat.id)]['Place']}\n"
                    f"Дата: {variables.feed_back[str(message.chat.id)]['Date']}\n"
                    f"Конфликт: {feedback_user}\n---------------------"
                )

                bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Laboratoriya xizmatini nazorat qilish SwissLab. Biz tanlaganingiz uchun'
                                                   ' tashakkur uchun tashakkur va xizmatimiz sifatini yaxshilashga yordam bersangiz xursand bolamiz!\n'
                                                  f'{variables.emj.EMJ_RAISING_HAND} Agar kerak bolsa, bizning operatorimiz sizga murojaat qiladi!')

                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(types.InlineKeyboardButton("Ответить", callback_data = f"Q{str(message.chat.id)}"))

                for id_p in variables.all_ids_arr: checkBlockedPeople(markup = markup, pers_id = id_p, txt = txt)

                database.insert_new_feedback_data(oper_id = '0', user_id = str(message.chat.id), txt = txt, bot = bot)
    
    elif feedback_user == 'stop': bot.send_message(message.chat.id, f'{variables.emj.EMJ_PLUS} Операция отменена' 
                                                  if lang == 0 else f'{variables.emj.EMJ_PLUS} Amal bekor qilindi')
                                                  
    else: nextStepWait(person_id = message.chat.id, text = f'{variables.emj.EMJ_PLUS} Введите ваш отзыв в правильном формате или напишите stop' if lang == 0 
                                                      else f'{variables.emj.EMJ_PLUS} Iltimos, sharhingizni togri formatda kiriting yoki yozing stop', func = fdBack_fill, args = [lang])


def enterTag(message, mess):
    global account
    if mess == "new":
        database.change_account_data(account = account[str(message.chat.id)], parametr = 'tags', data = [])        
        account = database.get_accounts_data()

    account[str(message.chat.id)].tags.append(message.text)
    database.change_account_data(account = account[str(message.chat.id)], parametr = 'tags', data = account[str(message.chat.id)].tags)       

    it = len(account[str(message.chat.id)].tags)
    send = bot.send_message(message.chat.id, f"{variables.emj.EMJ_PLUS} Введено {str(it)} из 10 пользователей")
    if it < 10: bot.register_next_step_handler(send, enterTag, "")
    else: bot.send_message(message.chat.id, f"{variables.emj.EMJ_EXCLAMATION} Вы получите скидку после того как пользователи активируют бота\n"
                                            f"{variables.emj.EMJ_EXCLAMATION} Если хотите изменить список друзей нажмите на /tags")
def enterTag_Sec(message, mess):
    global account
    if mess == "new":
        database.change_account_data(account = account[str(message.chat.id)], parametr = 'tags', data = [])        
        account = database.get_accounts_data()

    account[str(message.chat.id)].tags.append(message.text)
    database.change_account_data(account = account[str(message.chat.id)], parametr = 'tags', data = account[str(message.chat.id)].tags)

    it = len(account[str(message.chat.id)].tags)
    send = bot.send_message(message.chat.id, f"{variables.emj.EMJ_PLUS} Kirilgan {str(it)} 10 foydalanuvchilar")
    if it < 10: bot.register_next_step_handler(send, enterTag_Sec, "")
    else: bot.send_message(message.chat.id, f"{variables.emj.EMJ_EXCLAMATION} Foydalanuvchilar botni aktivlashtirgandan so'ng chegirmaga"
                                             " ega bo'lasiz agar do'stlaringiz ro'yxatini o'zgartirmoqchi bo'lsangiz bosing /tags")


def refAdd(message):
    global account
    account = database.get_accounts_data()
    if True in [True for person_id in account.keys() if person_id == message.text]:
        if int(account[message.text].ref) < 10:
            
            account[message.text].ref = str(int(account[message.text].ref) + 1)
            database.change_account_data(account = account[message.text], parametr = 'ref', data = str(int(account[message.text].ref) + 1))
            account = database.get_accounts_data()
            
            bot.send_message(message.chat.id, f"{variables.emj.EMJ_DONE} Спасибо за активацию!" if langCheck(message) 
                                         else f"{variables.emj.EMJ_DONE} Faollashtirish uchun rahmat!")
            bot.send_message(message.text, f"{variables.emj.EMJ_DONE} Новый пользователь активировал реферальный код!" if langCheck(message) 
                                      else f"{variables.emj.EMJ_DONE} Yangi foydalanuvchi tavsiya kodini faollashtirdi!")
                                      
            keyboardRefMaker(message = message, lang = 0 if langCheck(message) else 1)
        else:
            bot.send_message(message.chat.id, "⚠️ Активации кода закончены" if langCheck(message) else "⚠️ Kodni faollashtirish tugadi")
            keyboardRefMaker(message = message, lang = 0 if langCheck(message) else 1)
    elif message.text == "stop": keyboardRefMaker(message, 0 if langCheck(message) else 1)
    else: nextStepWait(person_id = message.chat.id, text = f'{variables.emj.EMJ_QUESTION} Ваш код не найден, поробуйте ещё раз или напишите - stop' if langCheck(message) 
                                                      else f'{variables.emj.EMJ_QUESTION} Sizning kodingiz topilmadi, yana porobuyte yoki yozing - stop', func = refAdd)

def userSebdText(message):
    global account
    if message.text != 'stop':
        if langCheck(person_id = account[str(message.chat.id)].feedback_st):
            bot.send_message(account[str(message.chat.id)].feedback_st, f"Ответ оператора #{account[str(message.chat.id)].feedback_st} на вашу жалобу!👇")
        else:  
            bot.send_message(account[str(message.chat.id)].feedback_st, f"Sizning shikoyatingizga javob beruvchi operator"
                                                                                 f" #{account[str(message.chat.id)].feedback_st} !👇")
        if message.photo != None:
            file_info = bot.get_file(message.photo[-1].file_id)
            bot.send_photo(account[str(message.chat.id)].feedback_st, bot.download_file(file_info.file_path))
        if message.text != None or message.caption != None:
            word_user_send = message.text if message.text != None else message.caption
            bot.send_message(account[str(message.chat.id)].feedback_st, word_user_send)
            database.insert_new_feedback_data(str(message.chat.id), account[str(message.chat.id)].feedback_st, word_user_send, bot)
        bot.send_message(message.chat.id, "Сообщение отправлено!")
        
        database.change_account_data(account = account[account[str(message.chat.id)].feedback_st], parametr = 'feedback_st', data = 'close')
        database.change_account_data(account = account[str(message.chat.id)], parametr = 'feedback_st', data = 'close')        
        account = database.get_accounts_data()

    else: bot.send_message(message.chat.id, 'Операция отменена!')


def inlineMessages(markup_text, call = None, message = None, person_id = None, markup_arr = [], action = True):
    """
      This definition make and push markup.
      param: markup_arr = [[text1, callback_data1], [text2, callback_data2]]
      param: action -> activate delete_message
    """
    person_id = person_id if person_id != None else message.chat.id if message != None else call.message.chat.id
    if action: bot.delete_message(person_id, call.message.message_id if call != None else message.message_id)
    markup = types.InlineKeyboardMarkup(row_width = 2)
    markup.add(*[types.InlineKeyboardButton(text = row[0], callback_data = row[1]) for row in markup_arr])
    bot.send_message(person_id, markup_text, reply_markup=markup)

def handlingdbCollection(message, call, data = ''):
    for line, row in zip(variables.add_text_dict, database.dbCollection(message = message, person_id = message.chat.id, step = variables.call_data_dict[call.data][1], action = 'show_data')[-1]):
                data += f"{line} {row}\n"
    bot.send_message(message.chat.id, data)
    inlineMessages(markup_text = 'Можете отправить отчёт или изменить данные', message = message, markup_arr = [['Отправить отчёт', 'Отправить отчёт'] 
                                                                                                  if checkOperId(person_id = str(message.chat.id), 
                                                                                                                 action    = variables.collection_oper_ids_arr) 
                                                                                                  else ['Подтвердить', 'Подтвердить'], ['Изменить', 'Изменить']])

def nextStepWait(person_id, text, func, args = None, action = False, message_id = None):
    if action: bot.delete_message(person_id, message_id)
    if args != None: bot.register_next_step_handler(bot.send_message(person_id, text), func, *args)
    else: bot.register_next_step_handler(bot.send_message(person_id, text), func)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global account
    try:
        if call.data in variables.call_data_dict.keys():
            if variables.call_data_dict[call.data][0] == 'set_lang':
                database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'language', data = call.data)
                account = database.get_accounts_data()
                inlineMessages(markup_text = openfileforRead(None, variables.call_data_dict[call.data][1]), call = call, 
                               markup_arr = variables.call_data_dict[call.data][2])
            
            elif variables.call_data_dict[call.data][0] == 'disagree_data':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, variables.call_data_dict[call.data][1])
            
            elif variables.call_data_dict[call.data][0] == 'agree_data':
                inlineMessages(markup_text = variables.call_data_dict[call.data][1], call = call, 
                               markup_arr = variables.call_data_dict[call.data][2])
            
            elif variables.call_data_dict[call.data][0] == 'no_code':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                keyboardRefMaker(call.message, variables.call_data_dict[call.data][1])
            
            elif variables.call_data_dict[call.data][0] == 'has_code':
                nextStepWait(person_id = call.message.chat.id, text = variables.call_data_dict[call.data][1], func = refAdd, args = None, action = True, 
                             message_id = call.message.message_id)
            
            elif variables.call_data_dict[call.data][0] == 'feedback':
                nextStepWait(person_id  = call.message.chat.id, text = variables.call_data_dict[call.data][1], func = fdbackName, 
                             args       = [variables.call_data_dict[call.data][2]], action = True, 
                             message_id = call.message.message_id)
            
            elif variables.call_data_dict[call.data][0] == 'friends_tag':
                nextStepWait(person_id  = call.message.chat.id, text = variables.call_data_dict[call.data][1], func = enterTag, args = ["new"], action = True, 
                             message_id = call.message.message_id)
            
            elif variables.call_data_dict[call.data][0] == 'edit_label':
                inlineMessages(markup_text = 'Выберите язык блока', call = call, markup_arr = variables.call_data_dict[call.data][1])
            
            elif variables.call_data_dict[call.data][0] == 'edit_label_sec':
                nextStepWait(person_id  = call.message.chat.id, text = f'{variables.emj.EMJ_PLUS} Введите текст для изменения', func = saveNewText, 
                             args       = [variables.call_data_dict[call.data][1]], action = True, 
                             message_id = call.message.message_id)
            
            elif variables.call_data_dict[call.data][0] == 'office_edit':
                nextStepWait(person_id = call.message.chat.id, text = f"{variables.emj.EMJ_PLUS} Введите данные для изменения", func = handlingdbCollection, 
                             args      = [call], action = True, 
                             message_id = call.message.message_id)
        
        elif call.data == '👍' or call.data == '👎':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Спасибо за оценку!' if langCheck(person_id = call.message.chat.id) else 'Baholash uchun rahmat!')
        elif call.data == 'Изменить': 
            inlineMessages(markup_text = 'Что нужно исправить?', call = call, markup_arr = variables.markup_change_collection_arr)
        elif call.data == 'Отправить отчёт' or call.data == 'Подтвердить':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            database.dbCollection(call.message, person_id = call.message.chat.id, action = 'send_collection_to_oper' if call.data == 'Отправить отчёт' else 'confirm_collection')
            bot.send_message(call.message.chat.id, 'Отчёт отправлен!' if call.data == 'Отправить отчёт' else 'Отчёт подтверждён!')
            keyboardRefMaker(call.message, 0 if langCheck(person_id = str(call.message.chat.id)) else 1, str(call.message.chat.id))
        elif call.data[0] == 'Q':
            if account[call.data[1:]].feedback_st == 'open':
                
                database.change_account_data(account = account[call.data[1:]], parametr = 'feedback_st', data = 'close')        
                database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'feedback_st', data = call.data[1:])
                account = database.get_accounts_data()

                nextStepWait(person_id = call.message.chat.id, text = f"{variables.emj.EMJ_PLUS} Введите текст для ответа пользователю", func = userSebdText)
            else:
                bot.send_message(call.message.chat.id, "Оператор уже ответил этому пользователю!\n"
                                                       "Для отмены повторного ответа напишите stop")
                
                database.change_account_data(account = account[call.data[1:]], parametr = 'feedback_st', data = 'close')        
                database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'feedback_st', data = call.data[1:])
                account = database.get_accounts_data()

                nextStepWait(person_id = call.message.chat.id, text = f"{variables.emj.EMJ_PLUS} Введите текст для ответа пользователю", func = userSebdText)
        else:
            if account[str(call.message.chat.id)].conversation == 'close':
                for k in account.keys():
                    if k == call.data and account[k].conversation == 'mid':
                        markup = markupMaker(action = 'redirect', button_text = variables.buttons_oper_text)
                        account[str(call.message.chat.id)].tags.append(str(k))
                        database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'tags', 
                                                     data = account[str(call.message.chat.id)].tags)        
                        database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'conversation', 
                                                     data = 'open')
                        database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'timer_conv', 
                                                     data = int(time.time()))
                        account[k].tags.append(str(call.message.chat.id))
                        account[k].tags.append("0")
                        database.change_account_data(account = account[k], parametr = 'tags', data = account[k].tags)        
                        database.change_account_data(account = account[k], parametr = 'conversation', data = 'open')
                        database.change_account_data(account = account[k], parametr = 'timer_conv', data = int(time.time()))
                        account = database.get_accounts_data()
                        if langCheck(person_id = k): bot.send_message(k, f"{variables.emj.EMJ_TELEPHONE} Найден оператор #{str(call.message.chat.id)}, переписка активирована")
                        else: bot.send_message(k, f"{variables.emj.EMJ_TELEPHONE} Operator #{str(call.message.chat.id)} topildi, yozishmalar faollashtirildi")
                        bot.send_message(str(call.message.chat.id), f"{variables.emj.EMJ_TELEPHONE} Вы подтвердили заявку!", reply_markup=markup)
                        db_answer = database.insert_new_data(str(k), str(call.message.chat.id))
                        bot.send_message(str(k)                   , db_answer)
                        bot.send_message(str(call.message.chat.id), db_answer)
                        break
                if account[str(call.message.chat.id)].conversation != 'open':
                    if account[str(call.data)].conversation != 'open':
                        bot.send_message(call.message.chat.id, f"Пользователь id: {str(call.data)} отменил режим!\nПовторный вызов...")
                        
                        markup = markupMaker(action = 'redirect', button_text = variables.buttons_oper_text)
                        user_markup = markupMaker(action = 'person', button_text = variables.buttons_oper_text if langCheck(person_id = str(call.data)) else variables.buttons_user_uz_text)
                        
                        account[str(call.message.chat.id)].tags.append(str(call.data))
                        database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'tags', data = account[str(call.message.chat.id)].tags)
                        database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'conversation', data = 'open')
                        database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'timer_conv', data = int(time.time()))

                        account[str(call.data)].tags.append(str(call.message.chat.id))
                        database.change_account_data(account = account[str(call.data)], parametr = 'tags', data = account[str(call.data)].tags)
                        
                        account[str(call.data)].tags.append("0")
                        database.change_account_data(account = account[str(call.data)], parametr = 'tags', data = account[str(call.data)].tags)
                        database.change_account_data(account = account[str(call.data)], parametr = 'conversation', data = 'open')
                        database.change_account_data(account = account[str(call.data)], parametr = 'timer_conv', data = int(time.time()))
                        account = database.get_accounts_data()

                        try:
                            if langCheck(person_id = str(call.data)): bot.send_message(str(call.data), f"{variables.emj.EMJ_TELEPHONE} Оператор"
                                                                                                       f" #{str(call.message.chat.id)} активировал переписку", 
                                                                                                       reply_markup=user_markup)
                            else: bot.send_message(str(call.data), f"{variables.emj.EMJ_TELEPHONE} Operator #{str(call.message.chat.id)} yozishmalarni faollashtirdi", 
                                                                                                       reply_markup=user_markup)
                            bot.send_message(str(call.message.chat.id), f"{variables.emj.EMJ_TELEPHONE} Вы подтвердили заявку!", reply_markup=markup)
                            db_answer = database.insert_new_data(str(call.data), str(call.message.chat.id))
                            bot.send_message(str(call.data)           , db_answer)
                            bot.send_message(str(call.message.chat.id), db_answer)
                        except Exception as e:
                            database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'conversation', data = 'close')
                            database.change_account_data(account = account[str(call.data)], parametr = 'tags', data = [])
                            database.change_account_data(account = account[str(call.message.chat.id)], parametr = 'tags', data = [])
                            account = database.get_accounts_data()
                            bot.send_message(call.message.chat.id, 'Пользователь выключил бота!')
                    else:
                        bot.send_message(str(call.message.chat.id), "Другой оператор отвечает на заявку!")
            else:
                bot.send_message(call.message.chat.id, "Закончите старый диалог, чтобы начать новый!")


    except Exception as error:
        debug.saveLogs(f"Error in the 'call' part!\n\n[\n{traceback.format_exc()}\n]", path.log_file)
        for id in variables.label_change_ids_arr:
            bot.send_message(int(id), f"Error in the 'call' part!\n\n{traceback.format_exc()}")

if __name__ == '__main__':
    Process(target = P_schedule.start_schedule, args = ()).start()
    try: bot.polling(none_stop=True)
    except Exception as _:
        debug.saveLogs(f"Program error!\n\n{traceback.format_exc()}", path.log_file)

        try:
            for id in variables.label_change_ids_arr:
                bot.send_message(int(id), f"Program error!\n\n{traceback.format_exc()}")
        except Exception as _:
            pass