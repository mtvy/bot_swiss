#/==================================================================\#
#                                                                    #
#\==================================================================/#

#\==================================================================/#
#/========================/ installed libs \========================\#

import traceback, \
         schedule, \
           telebot, \
               time, \
                  io, \
                  os
from PIL import Image,  \
            ImageDraw,   \
            ImageFont 

from multiprocessing import Process
from telebot import types

#--------------------------\ project files /-------------------------#

from variables import *
from database import *
from utility import *
from classes import *
from debug import *
from path import *
from emj import * 

#\==================================================================/#


#\==================================================================/#
TOKEN = '5361529726:AAHkDG9SoOJUA_1F9rWnIjTXkxW_kpq4vQg'
#\==================================================================/#


#\==================================================================/#
accounts = get_accounts()
#\==================================================================/#

#\==================================================================/#
def openfileforRead(action = None, file = None, text = '') -> str:
    return text.join([i for i in io.open(file, encoding='utf-8')])

def langCheck(account, message = None, id = None) -> bool:
    """
    This def returns True if the language is Russian.
    """
    return True if account[str(message.chat.id) if id == None else str(id)].language == "Русский" else False

def saveNewText(message, file) -> None:
    bot.send_message(message.chat.id, changes_message[saveText(message.text, file, 'w')])

def checkOperId(person_id, action) -> bool:
    """
    Use this method to check the role of a person.
    Parameters below described in py
    
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
#\==================================================================/#


#\==================================================================/#
bot = telebot.TeleBot(TOKEN)
#\==================================================================/#


#\==================================================================/#
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
        message_id = dbMessageId(action = 'take_id')[0][0]
        account = get_accounts()
        for account in account.keys():
            try:
                bot.forward_message(int(account), CHANNEL_ID, message_id)
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
                bot.forward_message(281321076, CHANNEL_ID, message_id)
                dbMessageId(action = 'save_id', message_id = message_id + 1)
            except Exception as error:
                print(f"Error pushing news!\n\n{repr(error)}")
                for id_er in label_change_ids_arr:
                    bot.send_message(int(id_er), f"Error pushing news!\n\n{repr(error)}")
#\==================================================================/#


#\==================================================================/#
@bot.message_handler(commands=['start'])
def welcome(message):
    global accounts
    
    accounts = get_accounts()

    _accounts = [str(message.chat.id)]
    
    for key in accounts.keys():
        if accounts[key].telegram_id == _accounts[0]:
            if accounts[key].language == "Русский":
                if accounts[key].personal_data == "YES":
                    bot.send_message(message.chat.id,
                        f"{EMJ_DOCTOR}Вы уже зарегистрированы в системе!"
                    )
                    keyboardRefMaker(message, 0)
                elif accounts[accounts].personal_data == "NO":
                    inlineMessages(
                        markup_text = openfileforRead(None, first_lang), 
                        message     = message, 
                        markup_arr  = [["Согласен"   , "Согласен"   ], 
                                       ["Отказываюсь", "Отказываюсь"]], 
                        action      = False
                    )
            elif accounts[accounts].language == "Ozbek":
                if accounts[accounts].personal_data == "YES":
                    bot.send_message(message.chat.id,
                        "🔱Siz allaqachon ro'yxatdan o'tgansiz!"
                    )
                    keyboardRefMaker(message = message, lang = 1)
                elif accounts[accounts].personal_data == "NO":
                    inlineMessages(
                        markup_text = openfileforRead(None, second_lang), 
                        message     = message,
                        markup_arr  = [["ROZIMAN"      , "Agree"   ], 
                                       ["Qo'shilmayman", "Disagree"]], 
                        action      = False
                    )
            else:
                inlineMessages(
                    markup_text = "🔱Choose language", 
                    message     = message, 
                    markup_arr  = [["Русский", "Русский"], 
                                   ["Ozbek", "Ozbek"]], 
                    action      = False
                )
            break
    else:
        _accounts += [str(message.chat.username)    , 
                      str(message.chat.first_name) , 
                      []                          , 
                      'close'                    , 
                      '0'                       , 
                      []                       , 
                      '0'                     ,  
                      'NO'                   , 
                      None                  , 
                      'close'              , 
                      0
        ]
        account = Account(_accounts)
        insert_account(account)
        accounts[account.telegram_id] = account
        inlineMessages(
            markup_text = "🔱Choose language", 
            msg         = message, 
            markup_arr  = [["Русский", "Русский"], 
                           ["Ozbek"  , "Ozbek"]], 
            action      = False
        )
#\==================================================================/#


#\==================================================================/#
@bot.message_handler(commands=['changeLabel'])
def adderNewLabel(message) -> None:
    if checkOperId(str(message.chat.id), label_change_ids_arr):
        inlineMessages(
            markup_text = "Какой блок надо отредактировать?", 
            msg = message, 
            markup_arr = markup_change_label_arr, 
            action = False
        )
#\==================================================================/#


#\==================================================================/#
def sendReqtoOper(which_oper, oper_send_text, markup) -> None:
    for oper_id in action_oper_select[which_oper]:
        bot.send_message(int(oper_id), 
            oper_send_text, 
            reply_markup=markup
        )

def operKeyboardMaker(message, which_oper, lang) -> None:
    global accounts

    accounts[str(message.chat.id)].conversation = 'mid'
    message_ids_dict[str(message.chat.id)] = message

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(f"{EMJ_BACK_ARROW} Отклонить вызов оператора" 
            if lang == 0 else f"{EMJ_BACK_ARROW} Operator chaqiruvini rad etish"
        ), 
        types.KeyboardButton(f"{EMJ_QUESTION} Инструкция" 
            if lang == 0 else f"{EMJ_QUESTION} Ko'rsatma"
        )
    )

    bot.send_message(message.chat.id, f"{EMJ_RAISING_HAND} Включён режим переписки с оператором" 
                    if lang == 0 else f"{EMJ_RAISING_HAND} Operator bilan yozishmalar rejimi yoqilgan", reply_markup=markup)

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Принять", callback_data=str(message.chat.id)))
    
    insert_message(message.chat.id, 0)

    sendReqtoOper(which_oper = which_oper, oper_send_text = (f"-------Запрос переписки!-------\n"
                                                             f"id: {message.chat.id} \n"
                                                             f"Имя: {message.chat.first_name} \n"
                                                             f"Фамилия: {message.chat.last_name} \n"
                                                             f"Username: @ {message.chat.username} \n"
                                                             f"Язык: Русский\n----------------------------"), markup = markup)

def dbDateSortEnter(message, action):
    nextStepWait(person_id = message.chat.id, text = db_conv_message['date'], func = dbSortEnter, args = [action])
def dbSortEnter(message, action):
    date_text = get_data(date = message.text, action = action)
    if date_text: 
        bot.send_message(message.chat.id, db_conv_message['no_date'])
    else:
        bot.send_message(message.chat.id, date_text)
        nextStepWait(person_id = message.chat.id, text = db_conv_message['name'], func = dbIdSortEnter, args = [action])
def dbIdSortEnter(message, action):
    id_text = get_text(message.text, action)
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
        
        update_account(account = account[account[str(message.chat.id)].tags[0]], parametr = 'conversation', data = 'close')
        update_account(account = account[account[str(message.chat.id)].tags[0]], parametr = 'tags', data = [])        
        account = get_accounts()

        keyboardRefMaker(message = message, lang = 0 if langCheck(message) else 1, pers_id = account[str(message.chat.id)].tags[0])

    keyboardRefMaker(message = message, lang = 0)
    inlineMessages(markup_text = 'Оцените работу оператора!' if langCheck(message) else 'Operator ishini baholang!', 
                   person_id = account[str(message.chat.id)].tags[0] if checkOperId(person_id = str(message.chat.id), 
                   action = all_ids_arr) else str(message.chat.id), markup_arr = [["👍", "👍"], ["👎", "👎"]], action = False)

   
def stopConversation(message, lang, pers_id=None, action = None):
    global account
    person_id = pers_id if pers_id != None else str(message.chat.id)
    push_text = f"{EMJ_EXCLAMATION} Завершение диалога" if lang == 0 or lang == 'Русский' else f"{EMJ_EXCLAMATION} Muloqotni yakunlash"
    bot.send_message(person_id, push_text)
    if len(account[person_id].tags) != 0:
        bot.send_message(str(account[person_id].tags[0]), push_text)
            
        update_account(account = account[account[person_id].tags[0]], parametr = 'conversation', data = 'close')
        update_account(account = account[account[person_id].tags[0]], parametr = 'tags', data = [])        
        account = get_accounts()

        keyboardRefMaker(None, 0 if account[account[person_id].tags[0]].language == "Русский" else 1, account[person_id].tags[0])
    keyboardRefMaker(None, lang, person_id)
    
    if not checkOperId(person_id = person_id, action = all_ids_arr):
        user_id = account[person_id].tags[0] if checkOperId(person_id = person_id, action = all_ids_arr) and action == None else person_id
        inlineMessages(markup_text = 'Оцените работу оператора!' if langCheck(person_id = user_id) else 'Operator ishini baholang!', 
                       person_id = user_id, markup_arr = [['👍', '👍'], ['👎', '👎']], action = False)
            
    update_account(account = account[person_id], parametr = 'conversation', data = 'close')
    update_account(account = account[person_id], parametr = 'tags', data = [])        
    account = get_accounts()
            
    change_status(person_id)

def closeConversation(message):
    global account
            
    update_account(account = account[str(message.chat.id)], parametr = 'conversation', data = 'close')
    update_account(account = account[str(message.chat.id)], parametr = 'tags', data = [])        
    account = get_accounts()
            
    change_status(message.chat.id)


def setCollectionKeyboard(message, person_id, show_text = 'Выберите необходимый мед офис'):
    bot.send_message(person_id, show_text, reply_markup = markupMaker(action = 'office', button_text = office_markup_dict))

def selectOffice(message, person_id, step, push_text = '', data = ''):
    if checkOperId(person_id = person_id, action = collection_oper_ids_arr):
        if show_text_dict[step]:
            dbCollection(message = message, person_id = person_id, step = step - 1, database_push_data = message.text)
            nextStepWait(person_id = person_id, text = show_text_dict[step], func = selectOffice, args = [person_id, step + 1])
        else:
            dbCollection(message = message, person_id = person_id, step = step - 1, database_push_data = message.text)
            for line, row in zip(add_text_dict, dbCollection(message = message, person_id = person_id, step = step, database_push_data = 'admin')[-1]):
                data += f"{line} {row}\n"
            bot.send_message(person_id, data)
            inlineMessages(markup_text = 'Можете отправить отчёт или изменить данные', message = message, 
                           markup_arr = [['Отправить отчёт', 'Отправить отчёт'], ['Изменить', 'Изменить']])

    elif checkOperId(person_id = person_id, action = collection_cash_ids_arr):
        dbCollection(message = message, person_id = person_id, database_push_data = message.text, action = 'cashier_init')
        database_data = dbCollection(message = message, person_id = person_id, database_push_data = message.text, step = 9, action = 'show_collection_to_cashier')
        if len(database_data) > 0:
            for line, row in zip(add_text_dict, database_data[-1]):
                data += f"{line} {row}\n"
            bot.send_message(person_id, data)
            inlineMessages(markup_text = 'Можете подтвердить или изменить данные', message = message, markup_arr = [['Подтвердить', 'Подтвердить'], ['Изменить', 'Изменить']])
        else:
            bot.send_message(person_id, 'Данных по этому офису нет!')
#\==================================================================/#


#\==================================================================/#
@bot.message_handler(content_types=['text', 'photo'])
def lol(message):
    global account
    account = get_accounts()
    
    if message.chat.type == 'private':
        if message.text in message_text_dict.keys():
            if   message_text_dict[message.text][0] == 'office': 
                selectOffice(message, str(message.chat.id), STEP_FIRST)
            elif message_text_dict[message.text][0] == 'text_show': 
                pushingLabelFromFile(message, message_text_dict[message.text][1], message_text_dict[message.text][2])
            elif message_text_dict[message.text][0] == 'oper_show': 
                operInit(message, message_text_dict[message.text][1], message_text_dict[message.text][2], str(message.chat.id))
            elif message_text_dict[message.text][0] == 'oper_close': 
                stopConversation(message, message_text_dict[message.text][1])
            elif message_text_dict[message.text][0] == 'redirect'  :
                redirectInit(message, f"{EMJ_EXCLAMATION} Общение завершено, перенаправление {message_text_dict[message.text][1]}")
                operInit(message_ids_dict[account[str(message.chat.id)].tags[0]], message_text_dict[message.text][2], 
                         message_text_dict[message.text][3], closeConversation(message))
        elif message.text == f'{EMJ_BACK_ARROW} Назад': 
            keyboardRefMaker(message = message, lang = account[str(message.chat.id)].language)
        elif message.text == f'{EMJ_EXCLAMATION} Оставить жалобу' or message.text == f'{EMJ_EXCLAMATION} Shikoyat qoldiring':
            if checkOperId(person_id = str(message.chat.id), action = feedback_oper_ids_arr): dbDateSortEnter(message = message, action = 'feedback_tb')
            else:
                account[str(message.chat.id)].feedback_st = 'open'
                inlineMessages(markup_text = openfileforRead(None, recv_label if langCheck(message) else sec_recv_label), message = message, 
                               markup_arr = [["Написать жалобу", "Написать жалобу"] if langCheck(message) else ["Shikoyat yozing", "Shikoyat yozing"]], action = False)
        elif message.text == f"{EMJ_MONEY_BAG} Инкассация": 
            setCollectionKeyboard(message = message, person_id = str(message.chat.id))
        elif message.text == f'{EMJ_DISK} БД переписок' or message.text == f'{EMJ_DISK} Yozishmalar bazasi':
            if checkOperId(person_id = str(message.chat.id), action = all_ids_arr): dbDateSortEnter(message = message, action = 'message_tb')
            else: bot.send_message(message.chat.id, 'У вас нет прав для чтения базы!' if langCheck(message) else "Sizda bazani o'qish huquqi yo'q!")
        elif message.text == '% Получить скидку' or message.text == '% Chegirma oling':
            if account[str(message.chat.id)].discount == "0" and account[str(message.chat.id)].ref == "0":
                bot.send_message(message.chat.id, openfileforRead(None, discount_label if langCheck(message) else sec_discount_label) + ("\nВаш реферальный код: " if langCheck(message) else  f"\nSizning tavsiyangiz kodi: ") + str(message.chat.id).format(message.chat, bot.get_me()),parse_mode='html')
            elif account[str(message.chat.id)].ref == "10":
                update_account(account = account[str(message.chat.id)], parametr = 'discount', data = '10')       
                account = get_accounts()
                bot.send_message(message.chat.id, f"{EMJ_DONE} У вас максимальная скидка!" if langCheck(message) 
                                             else f"{EMJ_DONE} Siz maksimal chegirma bor!")
                picPNGmaker(message)
            else:
                if account[str(message.chat.id)].discount == "10":
                    bot.send_message(message.chat.id, f"{EMJ_DONE} У вас максимальная скидка!" if langCheck(message) 
                                                 else f"{EMJ_DONE} Siz maksimal chegirma bor!")
                    picPNGmaker(message)
                else:
                    bot.send_message(message.chat.id, f"{EMJ_CROSS} Ваши друзья ещё не активировали бота!\n"
                                                      f"{EMJ_CROSS} Всего активаций {account[str(message.chat.id)].ref} из 10" if langCheck(message) 
                                                 else f"{EMJ_CROSS} Sizning do'stlaringiz hali botni faollashtirmagan!\n"
                                                      f"{EMJ_CROSS} Jami aktivatsiyalar {account[str(message.chat.id)].ref} dan 10")
                    picPNGmaker(message)
        elif message.text == f"{EMJ_EXCLAMATION} Жалоба":
            redirectInit(message, f"{EMJ_EXCLAMATION} Общение с оператором завершено, перенаправление в раздел жалоб")
            account[account[str(message.chat.id)].tags[0]].feedback_st = 'open'
            inlineMessages(markup_text = openfileforRead(None, recv_label if langCheck(message) else sec_recv_label), 
                           person_id = account[str(message.chat.id)].tags[0], markup_arr = [ ["Написать жалобу", "Написать жалобу"] if langCheck(message) 
                                                                                                 else ["Shikoyat yozing", "Shikoyat yozing"] ], action = False)
            closeConversation(message)        
        else:
            if account[str(message.chat.id)].conversation == 'open':
                if checkOperId(person_id = str(message.chat.id), action = all_ids_arr):
                    update_account(account = account[account[str(message.chat.id)].tags[0]], parametr = 'timer_conv', data = int(time.time()))
                    sm_id = 'Operator: '
                else:
                    update_account(account = account[str(message.chat.id)], parametr = 'timer_conv', data = int(time.time()))
                    sm_id = 'User: '
      
                account = get_accounts()

                if message.text != None:
                    sm_id = f'{sm_id}{message.text}\n'
                    bot.send_message(account[str(message.chat.id)].tags[0], message.text)
                elif message.caption != None:
                    sm_id = f'{sm_id}{message.caption}\n'
                    bot.send_message(account[str(message.chat.id)].tags[0], message.caption)
                if message.photo != None:
                    sm_id = f'{sm_id}PHOTO\n'
                    bot.send_photo(account[str(message.chat.id)].tags[0], bot.download_file(bot.get_file(message.photo[-1].file_id).file_path))
                insert_text(sm_id, message.chat.id)

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
                         if checkOperId(person_id = person_id, action = collection_cash_ids_arr + collection_oper_ids_arr) else 'oper' 
                         if checkOperId(person_id = person_id, action = all_ids_arr) else 'user', button_text = buttons_ru_text 
                         if lang or lang == 'Русский' else buttons_uz_text
                        )
    bot.send_message(person_id, openfileforRead(None, FAQ_label if lang == 0 or lang == 'Русский' else sec_FAQ_label) 
                                if not checkOperId(person_id, all_ids_arr) else 'Открыта клавиатура оператора!', parse_mode='html', reply_markup=markup)
    
    if person_id != pers_id:        
        account = get_accounts()
        update_account(account = account[str(message.chat.id)], parametr = 'personal_data', data = 'YES')
        account = get_accounts()


def checkBlockedPeople(markup, pers_id, txt):
    try: bot.send_message(pers_id, txt, reply_markup=markup)
    except Exception as error:
        for id_er in label_change_ids_arr:
            bot.send_message(int(id_er), f"User {pers_id} blocked!\n\n{repr(error)}")


def fdbackName(message, lang):
    global account
    name_user = message.text
    if name_user != 'stop':
        if name_user is None: name_user = 'Пользователь отправил нечитаемый объект'

        feed_back[str(message.chat.id)] = {
                                                     "Name" : name_user, 
                                                     "Username" : str(message.chat.username), 
                                                     "Language" : account[str(message.chat.id)].language
                                                    }
        nextStepWait(person_id = message.chat.id, text = f'{EMJ_PLUS} Введите ваш номер телефона' if lang == 0 
                                                    else f'{EMJ_PLUS} Telefon raqamingizni kiriting', func = fdbackTele, args = [lang])
    else:
        bot.send_message(message.chat.id, f'{EMJ_PLUS} Операция отменена')
def fdbackTele(message, lang):
    tele_num = message.text
    if tele_num.isdigit():

        feed_back[str(message.chat.id)].update({
                              'Telephone number' : tele_num if tele_num != None else 'Пользователь отправил нечитаемый объект'
                                                         })

        if lang: bot.send_message(message.chat.id, f'{EMJ_PLUS} Жалоба составляется в четыре этапа:\n'
                                                    '1) Причина жалобы и номер заявки\n'
                                                    '2) Обозначение филиала/места, где произошёл инцидент\n'
                                                    '3) Дата инцидента\n'
                                                    '4) Имя или опишите оппонента, с которым произошёл конфликт\n'
                                                   f'{EMJ_CROSS} Для отмены операции напишите stop')
        else:    bot.send_message(message.chat.id, f'{EMJ_PLUS} Shikoyat tort bosqichda tuziladi:\n'
                                                    '1) Shikoyat sababi\n'
                                                    '2) Hodisa sodir bolgan filial/joyni belgilash\n'
                                                    '3) Hodisa sanasi\n'
                                                    '4) Mojaro yuz bergan raqibning nomi yoki tarifi\n'
                                                   f'{EMJ_CROSS} Operatsiyani bekor qilish uchun yozing stop')
                                                                       
        nextStepWait(person_id = message.chat.id, text = f'{EMJ_PLUS} Напишите причину жалобы и номер заявки' 
                                       if lang == 0 else f'{EMJ_PLUS} Shikoyat sababini va ariza raqamini yozing', func = fdbackReason, args = [lang])
    elif tele_num == 'stop': bot.send_message(message.chat.id, f'{EMJ_PLUS} Операция отменена' 
                                             if lang == 0 else f'{EMJ_PLUS} Amal bekor qilindi')
    else: nextStepWait(person_id = message.chat.id, text = f'{EMJ_PLUS} Введите номер телефона в формате 998999999999 или напишите stop' 
                                         if lang == 0 else f'{EMJ_PLUS} Telefon raqamingizni formatda kiriting 9997777777777 yoki yozing stop', func = fdbackTele, args = [lang])
def fdbackReason(message, lang):
    reason_send = message.text
    if reason_send != 'stop':
        if reason_send == None: reason_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Reason" : reason_send})
        
        nextStepWait(person_id = message.chat.id, text = f'{EMJ_PLUS} Напишите филиал/место, где произошёл инцидент' 
                                       if lang == 0 else f'{EMJ_PLUS} Hodisa sodir bolgan filial/joyni yozing', func = fdbackPlace, args = [lang])
    else:
        bot.send_message(message.chat.id, f'{EMJ_PLUS} Операция отменена' 
                        if lang == 0 else f'{EMJ_PLUS} Amal bekor qilindi')  
def fdbackPlace(message, lang):
    place_send = message.text
    if place_send != 'stop':
        if place_send == None: place_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Place" : place_send})
        nextStepWait(person_id = message.chat.id, text = f'{EMJ_PLUS} Напишите дату инцидента' 
                                       if lang == 0 else f'{EMJ_PLUS} Hodisa tarixini yozing', func = fdbackDate, args = [lang])
    else: bot.send_message(message.chat.id, f'{EMJ_PLUS} Операция отменена' if lang == 0 else f'{EMJ_PLUS} Amal bekor qilindi')
def fdbackDate(message, lang):
    date_send = message.text
    if date_send != 'stop':
        feed_back[str(message.chat.id)].update({"Date" : date_send if date_send != None else 'Пользователь отправил нечитаемый объект'})
        nextStepWait(person_id = message.chat.id, text = f'{EMJ_PLUS} Напишите имя или опишите оппонента, с которым произошёл конфликт' 
                                       if lang == 0 else f'{EMJ_PLUS} Ismni yozing yoki ziddiyatga duch kelgan raqibni tariflang', func = fdBack_fill, args = [lang])
    else: bot.send_message(message.chat.id, f'{EMJ_PLUS} Операция отменена' 
                          if lang == 0 else f'{EMJ_PLUS} Amal bekor qilindi')
def fdBack_fill(message, lang):

    feedback_user = message.text

    if lang:
        if (feedback_user not in [
                    f'{EMJ_WRITING_HAND} Написать директору' ,  f'{EMJ_OLD_TELEPHONE} Тех. поддержка',
                    f'{EMJ_EXCLAMATION}️ Оставить жалобу'     ,  f'{EMJ_NOTE} Создать заказ'          ,
                    f'{EMJ_RAISING_HAND} Оператор'           ,  f'{EMJ_DISK} БД переписок'           ,
                    f'{EMJ_INFO} FAQ Инструкция'             ,  f'{EMJ_GLOBE} Соц. сети'             ,
                    f'{EMJ_TELEPHONE} Телефон'               ,  f'{EMJ_HOUSE} Адреса'                ,
                     '% Получить скидку'                                   ,  'stop'                                              ]
            ):
            
            if feedback_user is None: feedback_user = 'Пользователь отправил нечитаемый объект'

            feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})

            txt = (
                  f"--------ЖАЛОБА--------\n"
                  f"id: {str(message.chat.id)}\n"
                  f"Имя: {feed_back[str(message.chat.id)]['Name']}\n"
                  f"Язык: {account[str(message.chat.id)].language}\n"
                  f"Причина: {feed_back[str(message.chat.id)]['Reason']}\n"
                  f"Место: {feed_back[str(message.chat.id)]['Place']}\n"
                  f"Дата: {feed_back[str(message.chat.id)]['Date']}\n"
                  f"Конфликт: {feedback_user}\n---------------------"
            )

            bot.send_message(message.chat.id, f'{EMJ_PLUS} Контроль сервиса лаборатории SwissLab. Мы благодарим за'
                                               ' сделанный выбор и будем рады, если вы поможете улучшить качество нашего сервиса!\n'
                                              f'{EMJ_RAISING_HAND} Наш оператор свяжется с вами при необходимости!')

            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("Ответить", callback_data = f"Q{str(message.chat.id)}"))
            
            for id_p in all_ids_arr:
                checkBlockedPeople(markup = markup, pers_id = id_p, txt = txt)

            db_answer = insert_feedback(0, message.chat.id, txt)
            bot.send_message(message.chat.id, db_answer)

        elif (
                feedback_user not in [
                    f"{EMJ_OLD_TELEPHONE} O'sha.  qo'llab-quvvatlash" , f'{EMJ_EXCLAMATION} Shikoyat qoldiring',
                    f'{EMJ_GLOBE} Biz ijtimoiy tarmoqlarda'           , f'{EMJ_DISK} Yozishmalar bazasi'       ,
                    f'{EMJ_WRITING_HAND} Direktorga yozing'           , f"{EMJ_INFO} FAQ Ko'rsatma"            ,
                    f'{EMJ_NOTE} buyurtma yaratish'                   , f'{EMJ_TELEPHONE} telefon'             ,
                    f'{EMJ_RAISING_HAND} Operator'                    , f'{EMJ_HOUSE} manzillari'              ,
                     '% Chegirma oling'                                             ,  'stop' 
                ]
             ):

                if feedback_user == None: feedback_user = 'Пользователь отправил нечитаемый объект'
                
                feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})

                txt = (
                    f"--------ЖАЛОБА--------\n"
                    f"id: {str(message.chat.id)}\n"
                    f"Имя: {feed_back[str(message.chat.id)]['Name']}\n"
                    f"Язык: {account[str(message.chat.id)].language}\n"
                    f"Причина: {feed_back[str(message.chat.id)]['Reason']}\n"
                    f"Место: {feed_back[str(message.chat.id)]['Place']}\n"
                    f"Дата: {feed_back[str(message.chat.id)]['Date']}\n"
                    f"Конфликт: {feedback_user}\n---------------------"
                )

                bot.send_message(message.chat.id, f'{EMJ_PLUS} Laboratoriya xizmatini nazorat qilish SwissLab. Biz tanlaganingiz uchun'
                                                   ' tashakkur uchun tashakkur va xizmatimiz sifatini yaxshilashga yordam bersangiz xursand bolamiz!\n'
                                                  f'{EMJ_RAISING_HAND} Agar kerak bolsa, bizning operatorimiz sizga murojaat qiladi!')

                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(types.InlineKeyboardButton("Ответить", callback_data = f"Q{str(message.chat.id)}"))

                for id_p in all_ids_arr: checkBlockedPeople(markup = markup, pers_id = id_p, txt = txt)

                db_answer = insert_feedback(0, message.chat.id, txt, bot)
                bot.send_message(message.chat.id, db_answer)

    elif feedback_user == 'stop': bot.send_message(message.chat.id, f'{EMJ_PLUS} Операция отменена' 
                                                  if lang == 0 else f'{EMJ_PLUS} Amal bekor qilindi')
                                                  
    else: nextStepWait(person_id = message.chat.id, text = f'{EMJ_PLUS} Введите ваш отзыв в правильном формате или напишите stop' if lang == 0 
                                                      else f'{EMJ_PLUS} Iltimos, sharhingizni togri formatda kiriting yoki yozing stop', func = fdBack_fill, args = [lang])


def enterTag(message, mess):
    global account
    if mess == "new":
        update_account(account = account[str(message.chat.id)], parametr = 'tags', data = [])        
        account = get_accounts()

    account[str(message.chat.id)].tags.append(message.text)
    update_account(account = account[str(message.chat.id)], parametr = 'tags', data = account[str(message.chat.id)].tags)       

    it = len(account[str(message.chat.id)].tags)
    send = bot.send_message(message.chat.id, f"{EMJ_PLUS} Введено {str(it)} из 10 пользователей")
    if it < 10: bot.register_next_step_handler(send, enterTag, "")
    else: bot.send_message(message.chat.id, f"{EMJ_EXCLAMATION} Вы получите скидку после того как пользователи активируют бота\n"
                                            f"{EMJ_EXCLAMATION} Если хотите изменить список друзей нажмите на /tags")
def enterTag_Sec(message, mess):
    global account
    if mess == "new":
        update_account(account = account[str(message.chat.id)], parametr = 'tags', data = [])        
        account = get_accounts()

    account[str(message.chat.id)].tags.append(message.text)
    update_account(account = account[str(message.chat.id)], parametr = 'tags', data = account[str(message.chat.id)].tags)

    it = len(account[str(message.chat.id)].tags)
    send = bot.send_message(message.chat.id, f"{EMJ_PLUS} Kirilgan {str(it)} 10 foydalanuvchilar")
    if it < 10: bot.register_next_step_handler(send, enterTag_Sec, "")
    else: bot.send_message(message.chat.id, f"{EMJ_EXCLAMATION} Foydalanuvchilar botni aktivlashtirgandan so'ng chegirmaga"
                                             " ega bo'lasiz agar do'stlaringiz ro'yxatini o'zgartirmoqchi bo'lsangiz bosing /tags")


def refAdd(message):
    global account
    account = get_accounts()
    if True in [True for person_id in account.keys() if person_id == message.text]:
        if int(account[message.text].ref) < 10:
            
            account[message.text].ref = str(int(account[message.text].ref) + 1)
            update_account(account = account[message.text], parametr = 'ref', data = str(int(account[message.text].ref) + 1))
            account = get_accounts()
            
            bot.send_message(message.chat.id, f"{EMJ_DONE} Спасибо за активацию!" if langCheck(message) 
                                         else f"{EMJ_DONE} Faollashtirish uchun rahmat!")
            bot.send_message(message.text, f"{EMJ_DONE} Новый пользователь активировал реферальный код!" if langCheck(message) 
                                      else f"{EMJ_DONE} Yangi foydalanuvchi tavsiya kodini faollashtirdi!")
                                      
            keyboardRefMaker(message = message, lang = 0 if langCheck(message) else 1)
        else:
            bot.send_message(message.chat.id, "⚠️ Активации кода закончены" if langCheck(message) else "⚠️ Kodni faollashtirish tugadi")
            keyboardRefMaker(message = message, lang = 0 if langCheck(message) else 1)
    elif message.text == "stop": keyboardRefMaker(message, 0 if langCheck(message) else 1)
    else: nextStepWait(person_id = message.chat.id, text = f'{EMJ_QUESTION} Ваш код не найден, поробуйте ещё раз или напишите - stop' if langCheck(message) 
                                                      else f'{EMJ_QUESTION} Sizning kodingiz topilmadi, yana porobuyte yoki yozing - stop', func = refAdd)

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
            db_answer = insert_feedback(message.chat.id, int(account[str(message.chat.id)].feedback_st), word_user_send)
            bot.send_message(message.chat.id, db_answer)
        bot.send_message(message.chat.id, "Сообщение отправлено!")
        
        update_account(account = account[account[str(message.chat.id)].feedback_st], parametr = 'feedback_st', data = 'close')
        update_account(account = account[str(message.chat.id)], parametr = 'feedback_st', data = 'close')        
        account = get_accounts()

    else: bot.send_message(message.chat.id, 'Операция отменена!')


def inlineMessages(markup_text, call : Any    = None, 
                                msg  : Any    = None, 
                                _id  : int    = None, 
                                markup_arr    = [], 
                                action : bool = True) -> None:
    """
    ### This definition makes and pushes markup.
        param: markup_arr = [[text1, callback_data1], 
                             [text2, callback_data2]]
        param: action -> activate delete_message
    """
    try:
        if not _id and msg:
            _id = msg.chat.id
        elif not _id and not msg:
            _id = call.message.chat.id
    
        if action: 
            bot.delete_message(_id, 
                call.message.message_id if call != None 
                else msg.message_id
        )
        markup = types.InlineKeyboardMarkup(row_width = 2)
        markup.add(*[
            types.InlineKeyboardButton(
                text = row[0], 
                callback_data = row[1]
            ) for row in markup_arr]
        )
        bot.send_message(_id, 
            markup_text, reply_markup=markup
        )
    except:
        debug.saveLogs(f'[inlineMessages]---->{traceback.format_exc()}')

def handlingdbCollection(message, call, data = ''):
    for line, row in zip(add_text_dict, dbCollection(message = message, person_id = message.chat.id, step = call_data_dict[call.data][1], action = 'show_data')[-1]):
                data += f"{line} {row}\n"
    bot.send_message(message.chat.id, data)
    inlineMessages(markup_text = 'Можете отправить отчёт или изменить данные', message = message, markup_arr = [['Отправить отчёт', 'Отправить отчёт'] 
                                                                                                  if checkOperId(person_id = str(message.chat.id), 
                                                                                                                 action    = collection_oper_ids_arr) 
                                                                                                  else ['Подтвердить', 'Подтвердить'], ['Изменить', 'Изменить']])

def nextStepWait(person_id, text, func, args = None, action = False, message_id = None):
    if action: bot.delete_message(person_id, message_id)
    if args != None: bot.register_next_step_handler(bot.send_message(person_id, text), func, *args)
    else: bot.register_next_step_handler(bot.send_message(person_id, text), func)
#\==================================================================/#


#\==================================================================/#
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global accounts
    try:
        _data : str or Any = call.data
        _id   : int        = call.message.chat.id

        if _data in call_data_dict.keys():

            _key = call_data_dict[_data]

            if _key[0] == 'set_lang':
                update_account(accounts[str(_id)], 'language', _data)

                #accounts = get_accounts()

                inlineMessages(
                    markup_text = openfileforRead(None, _key[1]), 
                    call = call, 
                    markup_arr = _key[2]
                )
            
            elif _key[0] == 'disagree_data':
                bot.delete_message(_id, call.message.message_id)
                bot.send_message(_id, _key[1])
            
            elif _key[0] == 'agree_data':
                inlineMessages(
                    markup_text = _key[1], 
                    call = call, 
                    markup_arr = _key[2]
                )
            
            elif _key[0] == 'no_code':
                bot.delete_message(_id, call.message.message_id)
                keyboardRefMaker(call.message, _key[1])
            
            elif _key[0] == 'has_code':
                nextStepWait(
                    person_id  = _id, 
                    text       = _key[1], 
                    func       = refAdd, 
                    args       = None, 
                    action     = True, 
                    message_id = call.message.message_id
                )
            
            elif _key[0] == 'feedback':
                nextStepWait(
                    person_id  = _id, 
                    text       = _key[1], 
                    func       = fdbackName, 
                    args       = [_key[2]], 
                    action     = True, 
                    message_id = call.message.message_id
                )
            
            elif _key[0] == 'friends_tag':
                nextStepWait(
                    person_id  = _id, 
                    text       = _key[1], 
                    func       = enterTag, 
                    args       = ["new"], 
                    action     = True, 
                    message_id = call.message.message_id
                )
            
            elif _key[0] == 'edit_label':
                inlineMessages(
                    markup_text = 'Выберите язык блока', 
                    call        = call, 
                    markup_arr  = _key[1]
                )
            
            elif _key[0] == 'edit_label_sec':
                nextStepWait(
                    person_id  = _id, 
                    text       = f'{EMJ_PLUS} Введите текст для изменения', 
                    func       = saveNewText, 
                    args       = [_key[1]], 
                    action     = True, 
                    message_id = call.message.message_id
                )
            
            elif _key[0] == 'office_edit':
                nextStepWait(
                    person_id  = _id, 
                    text       = f"{EMJ_PLUS} Введите данные для изменения", 
                    func       = handlingdbCollection, 
                    args       = [call], 
                    action     = True, 
                    message_id = call.message.message_id
                )
        
        elif _data == '👍' or _data == '👎':
            bot.delete_message(_id, call.message.message_id)
            bot.send_message(_id, 
                'Спасибо за оценку!' if langCheck(person_id = _id) 
                                     else 'Baholash uchun rahmat!'
            )
        elif _data == 'Изменить': 
            inlineMessages(
                markup_text = 'Что нужно исправить?', 
                call = call, 
                markup_arr = markup_change_collection_arr
            )
        elif _data == 'Отправить отчёт' or _data == 'Подтвердить':
            bot.delete_message(_id, call.message.message_id)
            dbCollection(
                call.message, 
                person_id = _id, 
                action = 'send_collection_to_oper' if _data == 'Отправить отчёт' 
                                                   else 'confirm_collection'
            )
            bot.send_message(_id, 
                'Отчёт отправлен!' if _data == 'Отправить отчёт' 
                                   else 'Отчёт подтверждён!'
            )
            keyboardRefMaker(
                call.message, 
                0 if langCheck(person_id = str(_id)) else 1, 
                str(_id)
            )
        elif _data[0] == 'Q':
            if accounts[_data[1:]].feedback_st == 'open':
                update_account(
                    accounts[_data[1:]], 
                    'feedback_st',
                    'close'
                )        
                update_account(
                    accounts[str(_id)], 
                    'feedback_st', 
                    _data[1:]
                )
                
                accounts = get_accounts()

                nextStepWait(
                    person_id = _id, 
                    text = f"{EMJ_PLUS} Введите текст для ответа пользователю", 
                    func = userSebdText
                )
            else:
                bot.send_message(_id, 
                    "Оператор уже ответил этому пользователю!\n"
                    "Для отмены повторного ответа напишите stop"
                )
                
                update_account(
                    accounts[_data[1:]], 
                    'feedback_st', 
                    'close'
                )        
                update_account(
                    accounts[str(_id)], 
                    'feedback_st', 
                    _data[1:]
                )
                accounts = get_accounts()

                nextStepWait(
                    person_id = _id, 
                    text = f"{EMJ_PLUS} Введите текст для ответа пользователю", 
                    func = userSebdText
                )
        else:
            if accounts[str(_id)].conversation == 'close':
                for u_id in accounts.keys():
                    if u_id == _data and accounts[u_id].conversation == 'mid':
                        markup = markupMaker(
                            action = 'redirect', 
                            button_text = buttons_oper_text
                        )
                        accounts[str(_id)].tags.append(str(u_id))
                        update_account(
                            accounts[str(_id)], 
                            'tags', 
                            accounts[str(_id)].tags
                        )        
                        update_account(
                            accounts[str(_id)],
                            'conversation', 
                            'open'
                        )
                        update_account(
                            accounts[str(_id)], 
                            'timer_conv', 
                            int(time.time())
                        )
                        accounts[u_id].tags.append(str(_id))
                        accounts[u_id].tags.append("0")
                        update_account(
                            accounts[u_id], 
                            'tags', 
                            accounts[u_id].tags
                        )        
                        update_account(
                            accounts[u_id], 
                            'conversation', 
                            'open'
                        )
                        update_account(
                            accounts[u_id], 
                            'timer_conv', 
                            int(time.time())
                        )
                        accounts = get_accounts()

                        bot.send_message(u_id, 
                            f"{EMJ_TELEPHONE} Найден оператор #{str(_id)}, "
                            "переписка активирована" if langCheck(person_id = u_id) 
                            else 
                            f"{EMJ_TELEPHONE} Operator #{str(_id)} topildi, "
                            "yozishmalar faollashtirildi"
                        )
                        
                        bot.send_message(str(_id), 
                            f"{EMJ_TELEPHONE} Вы подтвердили заявку!",
                            reply_markup=markup
                        )
                        db_answer = insert_message(u_id, _id)

                        bot.send_message(str(u_id), db_answer)
                        bot.send_message(str( _id), db_answer)

                        break

                if accounts[str(_id)].conversation != 'open':
                    if accounts[str(_data)].conversation != 'open':
                        bot.send_message(_id, 
                            f"Пользователь id: {str(_data)} отменил режим!\n"
                            "Повторный вызов..."
                        )
                        
                        markup = markupMaker('redirect', buttons_oper_text)
                        user_markup = markupMaker('person', buttons_oper_text 
                            if langCheck(person_id = str(_data)) else buttons_user_uz_text
                        )
                        
                        accounts[str(_id)].tags.append(str(_data))
                        update_account(
                            accounts[str(_id)], 
                            'tags', 
                            accounts[str(_id)].tags
                        )
                        update_account(
                            accounts[str(_id)], 
                            'conversation', 
                            'open'
                        )
                        update_account(
                            accounts[str(_id)], 
                            'timer_conv', 
                            int(time.time())
                        )

                        accounts[str(_data)].tags.append(str(_id))
                        update_account(
                            accounts[str(_data)], 
                            'tags', 
                            accounts[str(_data)].tags
                        )
                        
                        accounts[str(_data)].tags.append("0")
                        update_account(
                            accounts[str(_data)], 
                            'tags', 
                            accounts[str(_data)].tags
                        )
                        update_account(
                            accounts[str(_data)], 
                            'conversation', 
                            'open')
                        update_account(
                            accounts[str(_data)], 
                            'timer_conv', 
                            int(time.time())
                        )
                        accounts = get_accounts()

                        try:
                            if langCheck(person_id = str(_data)): 
                                bot.send_message(str(_data), 
                                    f"{EMJ_TELEPHONE} Оператор"
                                    f" #{str(_id)} активировал переписку", 
                                    reply_markup=user_markup
                                )
                            else: 
                                bot.send_message(str(_data), 
                                    f"{EMJ_TELEPHONE} Operator #{str(_id)} "
                                    "yozishmalarni faollashtirdi", 
                                    reply_markup=user_markup
                                )

                            bot.send_message(str(_id), 
                                f"{EMJ_TELEPHONE} Вы подтвердили заявку!", 
                                reply_markup=markup
                            )
                            db_answer = insert_message(_data, _id)

                            bot.send_message(str(_data), db_answer)
                            bot.send_message(str(  _id), db_answer)
                        except:
                            update_account(
                                accounts[str(_id)], 
                                'conversation', 
                                'close'
                            )
                            update_account(accounts[str(_data)], 'tags', [])
                            update_account(accounts[str(  _id)], 'tags', [])

                            accounts = get_accounts()

                            bot.send_message(_id, 'Пользователь выключил бота!')
                    else:
                        bot.send_message(str(_id), 
                            "Другой оператор отвечает на заявку!"
                        )
            else:
                bot.send_message(_id, 
                    "Закончите старый диалог, чтобы начать новый!"
                )


    except:
        saveLogs(
            f"Error in the 'call' part!\n\n[\n{traceback.format_exc()}\n]"
        )
        for id in label_change_ids_arr:
            bot.send_message(int(id), 
                f"Error in the 'call' part!\n\n{traceback.format_exc()}"
            )
#\==================================================================/#


#\==================================================================/#
if __name__ == '__main__':
    Process(target = P_schedule.start_schedule, args = ()).start()
    try: 
        bot.polling(none_stop=True)
    except:
        saveLogs(f"Program error!\n\n{traceback.format_exc()}")
        try:
            for id in label_change_ids_arr:
                bot.send_message(int(id), 
                    f"Program error!\n\n{traceback.format_exc()}"
                )
        except:
            pass
#\==================================================================/#
