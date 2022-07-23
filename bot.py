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
from numpy import save
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

def isRu(_accs : Dict[str, Account], msg = None, id : int = None) -> bool:
    """
    This def returns True if the language is Russian.
    """
    return True if _accs[str(msg.chat.id) if id == None else str(id)].language == "Русский" else False

def saveNewText(message, file) -> None:
    bot.send_message(message.chat.id, changes_message[saveText(message.text, file, 'w')])

def checkOperId(person_id : str, action) -> bool:
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

def markupMaker(mode : str, button : Dict[str, str]) -> types.ReplyKeyboardMarkup():
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        pin = [types.KeyboardButton(tag) 
                for tag in button.keys() if mode in button[tag]]

        if mode not in ('user', 'redirect'): 
            markup.add(*pin) 
        elif mode != 'redirect':
            markup.row(      pin[0], pin[1], pin[3]
                ).row(           pin[5], pin[8]
                ).row(              pin[10]
                ).row(           pin[2], pin[7]
                ).row(           pin[4], pin[9]
            )
        else: 
            markup.row(          pin[0], pin[1]
                ).row(        pin[2], pin[3], pin[4]
                ).row(              pin[5:7]
            )
        return markup
    except:
        saveLogs(f'[markupMaker]---->{traceback.format_exc()}')

    return types.ReplyKeyboardMarkup(resize_keyboard=True)
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
                    stopConversation(message = None, lang = 0 if isRu(account, message = None, person_id = account) else 1, pers_id = account)
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
def welcome(msg):
    global accounts
    
    accounts = get_accounts()

    _accounts = [str(msg.chat.id)]

    _id = _accounts[0]

    if _id in accounts.keys():
        if not accounts[_id].language:
            inlineMessages(
                markup_text = "🔱Choose language", 
                msg         = msg, 
                markup_arr  = [["Русский", "Русский"], 
                               ["Ozbek", "Ozbek"]], 
                action      = False
            )
        elif accounts[_id].personal_data == 'YES':
            bot.send_message(msg.chat.id,
                f'{EMJ_DOCTOR}Вы уже зарегистрированы в системе!'
                if isRu(accounts, msg = msg) else
                "🔱Siz allaqachon ro'yxatdan o'tgansiz!"
            )
            keyboardRefMaker(msg, not isRu(accounts, msg = msg))
        elif accounts[_id].personal_data == 'NO':
            inlineMessages(
                markup_text = openfileforRead(None, 
                    first_lang if isRu(accounts, msg = msg) else second_lang
                ), 
                msg = msg, 
                markup_arr = [["Согласен"   , "Согласен"   ], 
                              ["Отказываюсь", "Отказываюсь"]] 
                              if isRu(accounts, msg = msg) else
                             [["ROZIMAN"      , "Agree"   ], 
                              ["Qo'shilmayman", "Disagree"]], 
                action = False
            )
    else:
        _accounts += [str(msg.chat.username)    , 
                      str(msg.chat.first_name) , 
                      []                      , 
                      'close'                , 
                      '0'                   , 
                      []                   , 
                      '0'                 ,  
                      'NO'               , 
                      None              , 
                      'close'          , 
                      0
        ]
        account = Account(_accounts)
        if insert_account(account):
            accounts[account.telegram_id] = account
            inlineMessages(
                markup_text = "🔱Choose language", 
                msg         = msg,
                markup_arr  = [["Русский", "Русский"] , 
                               ["Ozbek"  , "Ozbek"  ]], 
                action      = False
            )
        else:
            work_msg(msg.chat.id)
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
def sendReqtoOper(_oper : str, op_txt : str, markup) -> None:
    for oper_id in action_oper_select[_oper]:
        try:
            bot.send_message(int(oper_id), 
               op_txt, reply_markup=markup
            )
        
        except telebot.apihelper.ApiException:
            continue
        
        except:
            saveLogs(f'[sendReqtoOper]---->{traceback.format_exc()}')
        
def operKeyboardMaker(msg, which_oper, lang) -> None:
    global accounts

    _id : str = str(msg.chat.id)

    try:
        accounts[_id].conversation = 'mid'
        message_ids_dict[_id] = msg

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            types.KeyboardButton(
                f"{EMJ_BACK_ARROW} Отклонить вызов оператора" 
                if not lang else 
                f"{EMJ_BACK_ARROW} Operator chaqiruvini rad etish"
            ), 
            types.KeyboardButton(
                f"{EMJ_QUESTION} Инструкция" 
                if not lang else 
                f"{EMJ_QUESTION} Ko'rsatma"
            )
        )

        bot.send_message(_id, 
            f"{EMJ_RAISING_HAND} Включён режим переписки с оператором" 
            if not lang else 
            f"{EMJ_RAISING_HAND} Operator bilan yozishmalar rejimi yoqilgan", 
            reply_markup=markup
        )

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("Принять", callback_data=_id)
        )

        insert_message(msg.chat.id, 0)

        sendReqtoOper(which_oper, 
            f'-------Запрос переписки!-------  \n'
            f'id:        {msg.chat.id}         \n'
            f'Имя:       {msg.chat.first_name} \n'
            f'Фамилия:   {msg.chat.last_name}  \n'
            f'Username: @{msg.chat.username}   \n'
            f'Язык: Русский\n'
            '--------------------------------', 
            markup
        )
    except:
        saveLogs(f'[operKeyboardMaker]---->{traceback.format_exc()}')
        work_msg(_id)


def dbDateSortEnter(msg, mod) -> None:
    nextStepWait(
        _id = msg.chat.id, 
        txt = db_conv_message['date'], 
        func = dbSortEnter, 
        args = [mod]
    )
def dbSortEnter(msg, mod) -> None:
    date_text = get_data(msg.text, mod)

    if not date_text: 
        bot.send_message(msg.chat.id, db_conv_message['no_date'])
    else:
        bot.send_message(msg.chat.id, date_text)
        nextStepWait(
            _id = msg.chat.id, 
            txt = db_conv_message['name'], 
            func = dbIdSortEnter, 
            args = [mod]
        )
def dbIdSortEnter(msg, mod) -> None:
    id_text = get_text(msg.text, mod)
    bot.send_message(msg.chat.id, 
        id_text if id_text else 'Такого номера нет в базе!'
    )

def pushingLabelFromFile(msg, _accs, path1, path2) -> None:
    bot.send_message(msg.chat.id, 
        openfileforRead(None, path1 if isRu(_accs, msg = msg) else path2)
    )

def operInit(msg, accs, action, set_act):
    try:
        if checkOperId(str(msg.chat.id), action): 
            bot.send_message(msg.chat.id, "Вы оператор!")
        else: 
            operKeyboardMaker(msg, set_act, 0 if isRu(accs, msg) else 1)
    except:
        saveLogs(f'[operInit]---->{traceback.format_exc()}')
        work_msg(msg.chat.id)
        
def redirectInit(message, action):
    global account

    bot.send_message(str(message.chat.id), action)
    if len(account[str(message.chat.id)].tags) != 0:

        bot.send_message(str(account[str(message.chat.id)].tags[0]), action)
        
        update_account(account = account[account[str(message.chat.id)].tags[0]], parametr = 'conversation', data = 'close')
        update_account(account = account[account[str(message.chat.id)].tags[0]], parametr = 'tags', data = [])        
        account = get_accounts()

        keyboardRefMaker(message = message, lang = 0 if isRu(message) else 1, pers_id = account[str(message.chat.id)].tags[0])

    keyboardRefMaker(message = message, lang = 0)
    inlineMessages(markup_text = 'Оцените работу оператора!' if isRu(message) else 'Operator ishini baholang!', 
                   person_id = account[str(message.chat.id)].tags[0] if checkOperId(person_id = str(message.chat.id), 
                   action = all_ids_arr) else str(message.chat.id), markup_arr = [["👍", "👍"], ["👎", "👎"]], action = False)

   
def stopConversation(message, lang, _id = None, action = None) -> None:
    global accounts

    u_id : str = _id if _id != None else str(message.chat.id)

    push_text = f"{EMJ_EXCLAMATION} Завершение диалога" \
                if lang == 0 or lang == 'Русский' else  \
                f"{EMJ_EXCLAMATION} Muloqotni yakunlash"

    bot.send_message(u_id, push_text)

    acc : Account = accounts[u_id]

    if len(acc.tags):

        t_id : str = acc.tags[0]

        bot.send_message(t_id, push_text)

        t_acc : Account = accounts[t_id]
            
        update_account(t_acc, 'conversation', 'close')
        update_account(t_acc, 'tags', []) 

        keyboardRefMaker(None, 
            0 if t_acc.language == "Русский" else 1, t_id
        )
    
    keyboardRefMaker(None, lang, u_id)
    
    if not checkOperId(u_id, all_ids_arr):

        user_id = acc.tags[0] \
            if checkOperId(u_id, all_ids_arr) and action == None else u_id
            
        inlineMessages(
            markup_text = 'Оцените работу оператора!' 
                          if isRu(accounts, id = user_id) else 
                          'Operator ishini baholang!', 
            _id = user_id, 
            markup_arr = [['👍', '👍'], 
                          ['👎', '👎']], 
            action = False
        )
            
    update_account(acc, 'conversation', 'close')
    update_account(acc, 'tags', [])

    accounts = get_accounts()

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
def lol(msg) -> bool:
    global accounts

    try:

            accounts = get_accounts()

            _id : str = str(msg.chat.id)

            if _id in accounts.keys():
                acc : Account = accounts[_id]
            else:
                bot.send_message(_id, 
                    'Please restart the bot for authorization.'
                )
                return False

            if msg.chat.type == 'private' and acc.personal_data == 'YES':

                txt : str = msg.text

                if txt in message_text_dict.keys():

                    key : Dict = message_text_dict[txt]

                    if key[0] == 'office': 
                        selectOffice(msg, _id, STEP_FIRST)

                    elif key[0] == 'text_show': 
                        pushingLabelFromFile(msg, accounts, key[1], key[2])

                    elif key[0] == 'oper_show': 
                        operInit(msg, accounts, key[1], key[2])

                    elif key[0] == 'oper_close': 
                        stopConversation(msg, key[1])

                    elif key[0] == 'redirect':
                        redirectInit(msg, 
                            f"{EMJ_EXCLAMATION} Общение завершено, перенаправление {key[1]}"
                        )
                        operInit(message_ids_dict[acc.tags[0]], 
                            key[2], key[3], closeConversation(msg)
                        )

                elif txt == f'{EMJ_BACK_ARROW} Назад': 
                    keyboardRefMaker(msg, acc.language)

                elif txt in (f'{EMJ_EXCLAMATION} Оставить жалобу', 
                             f'{EMJ_EXCLAMATION} Shikoyat qoldiring'):

                    if checkOperId(_id, feedback_oper_ids_arr): 
                        dbDateSortEnter(msg, 'feedback_tb')
                    else:
                        acc.feedback_st = 'open'
                        inlineMessages(
                            markup_text = openfileforRead(None, 
                                recv_label if isRu(accounts, msg = msg) else sec_recv_label
                            ), 
                            msg = msg, 
                            markup_arr = [["Написать жалобу", 
                                           "Написать жалобу"] if isRu(msg) else 
                                          ["Shikoyat yozing", 
                                           "Shikoyat yozing"]
                            ], 
                            action = False
                        )

                elif txt == f"{EMJ_MONEY_BAG} Инкассация":
                    #setCollectionKeyboard(message = msg, person_id = _id)
                    work_msg(msg.chat.id)

                elif txt in (f'{EMJ_DISK} БД переписок', f'{EMJ_DISK} Yozishmalar bazasi'):
                    if checkOperId(_id, all_ids_arr): 
                        dbDateSortEnter(msg, 'message_tb')
                    else: 
                        bot.send_message(msg.chat.id, 
                            'У вас нет прав для чтения базы!' 
                            if isRu(msg) else 
                            'Sizda bazani o\'qish huquqi yo\'q!'
                        )

                elif txt in ('% Получить скидку', '% Chegirma oling'):
                    if isRu(accounts, msg):
                        bot.send_message(msg.chat.id, 
                            f'{openfileforRead(None, discount_label)}'
                            f'\nВаш реферальный код: {msg.chat.id}',
                        )
                    else:
                        bot.send_message(msg.chat.id, 
                            f'{openfileforRead(None, sec_discount_label)}'
                            f'\nSizning tavsiyangiz kodi: {msg.chat.id}',
                        )

                elif txt == f"{EMJ_EXCLAMATION} Жалоба":
                    redirectInit(msg, 
                        f'{EMJ_EXCLAMATION} Общение с оператором завершено, перенаправление в раздел жалоб'
                    )
                    accounts[acc.tags[0]].feedback_st = 'open'

                    inlineMessages(
                        markup_text = openfileforRead(None, recv_label if isRu(msg) else sec_recv_label), 
                        _id = acc.tags[0], 
                        markup_arr = [["Написать жалобу", 
                                       "Написать жалобу"] 
                                      if isRu(msg) else 
                                      ["Shikoyat yozing", 
                                       "Shikoyat yozing"]], 
                        action = False
                    )
                    closeConversation(msg)

                elif acc.conversation == 'open':
                    if checkOperId(_id, all_ids_arr):
                        update_account(accounts[acc.tags[0]], 
                            'timer_conv', int(time.time())
                        )
                        sm_id = 'Operator: '
                    else:
                        update_account(acc, 
                            'timer_conv', int(time.time())
                        )
                        sm_id = 'User: '

                    accounts = get_accounts()

                    if txt:
                        sm_id = f'{sm_id}{txt}\n'
                        bot.send_message(acc.tags[0], txt)
                    elif msg.caption:
                        sm_id = f'{sm_id}{msg.caption}\n'
                        bot.send_message(acc.tags[0], msg.caption)

                    if msg.photo:
                        sm_id = f'{sm_id}PHOTO\n'
                        bot.send_photo(acc.tags[0], 
                            bot.download_file(
                                bot.get_file(msg.photo[-1].file_id).file_path
                            )
                        )

                    insert_text(sm_id, msg.chat.id)
    except:
        saveLogs(f'[lol]---->{traceback.format_exc()}')
        work_msg(msg.chat.id)


def keyboardRefMaker(msg, lang, _id = None):
    global accounts
    try:
        u_id = _id if _id != None else str(msg.chat.id)
        markup = markupMaker('admin' 
            if checkOperId(u_id, collection_cash_ids_arr + collection_oper_ids_arr) else 'oper' 
            if checkOperId(u_id, all_ids_arr) else 'user', 
            buttons_ru_text if not lang or lang == 'Русский' else buttons_uz_text
        )
        bot.send_message(u_id, 
            openfileforRead(None, FAQ_label if not lang or lang == 'Русский' else sec_FAQ_label) 
            if not checkOperId(u_id, all_ids_arr) else 'Открыта клавиатура оператора!', 
            parse_mode='html', reply_markup=markup
        )
    except:
        saveLogs(f'[keyboardRefMaker]---->{traceback.format_exc()}')


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


def userSebdText(message):
    global account
    if message.text != 'stop':
        if isRu(person_id = account[str(message.chat.id)].feedback_st):
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
            del_msg(_id, 
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

def nextStepWait(_id, txt, func, args = None, mod = False, _msg_id = None):
    try:
        if mod: 
            del_msg(_id, _msg_id)
        if args:
            msg = bot.send_message(_id, txt)
            bot.register_next_step_handler(msg, func, *args)
        else:
            msg = bot.send_message(_id, txt)
            bot.register_next_step_handler(msg, func)
    except:
        saveLogs(f'[nextStepWait]---->{traceback.format_exc()}')


def del_msg(_id, _msg_id):
    try:
        bot.delete_message(_id, _msg_id)
    except:
        saveLogs(f'[del_msg]---->{error.format_exc()}')

def work_msg(_id : int) -> None:
    bot.send_message(_id, 
        'The service is temporarily unavailable. We apologize.'
    )
#\==================================================================/#


#\==================================================================/#
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global accounts
    try:
        _data : str or Any = call.data
        _id   : int        = call.message.chat.id
        m_id  : int        = call.message.message_id

        if _data in call_data_dict.keys():

            _key = call_data_dict[_data]

            if _key[0] == 'set_lang':
                if update_account(accounts[str(_id)], 'language', _data):

                    accounts = get_accounts()

                    inlineMessages(
                        markup_text = openfileforRead(None, _key[1]), 
                        call = call, 
                        markup_arr = _key[2]
                    )
                else:
                    work_msg(_id)
            
            elif _key[0] == 'disagree_data':
                del_msg(_id, m_id)
                bot.send_message(_id, _key[1])
            
            elif _key[0] == 'agree_data':
                if update_account(accounts[str(_id)], 'personal_data', 'YES'):

                    accounts = get_accounts()

                    inlineMessages(
                        markup_text = _key[1], 
                        call = call, 
                        markup_arr = _key[2]
                    )
                else:
                    work_msg(_id)
            
            elif _key[0] in ('no_code', 'has_code'):
                del_msg(_id, m_id)
                keyboardRefMaker(call.message, _key[1])
            
            elif _key[0] == 'feedback':
                nextStepWait(
                    person_id  = _id, 
                    text       = _key[1], 
                    func       = fdbackName, 
                    args       = [_key[2]], 
                    action     = True, 
                    message_id = m_id
                )
            
            elif _key[0] == 'friends_tag':
                nextStepWait(
                    person_id  = _id, 
                    text       = _key[1], 
                    func       = enterTag, 
                    args       = ["new"], 
                    action     = True, 
                    message_id = m_id
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
                    message_id = m_id
                )
            
            elif _key[0] == 'office_edit':
                nextStepWait(
                    person_id  = _id, 
                    text       = f"{EMJ_PLUS} Введите данные для изменения", 
                    func       = handlingdbCollection, 
                    args       = [call], 
                    action     = True, 
                    message_id = m_id
                )
        
        elif _data == '👍' or _data == '👎':
            del_msg(_id, m_id)
            bot.send_message(_id, 
                'Спасибо за оценку!' 
                if isRu(accounts, id = _id) else 
                'Baholash uchun rahmat!'
            )
        elif _data == 'Изменить': 
            inlineMessages(
                markup_text = 'Что нужно исправить?', 
                call = call, 
                markup_arr = markup_change_collection_arr
            )
        elif _data == 'Отправить отчёт' or _data == 'Подтвердить':
            del_msg(_id, m_id)
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
                0 if isRu(person_id = str(_id)) else 1, 
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
                            "переписка активирована" if isRu(person_id = u_id) 
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
                            if isRu(person_id = str(_data)) else buttons_user_uz_text
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
                            if isRu(person_id = str(_data)): 
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
