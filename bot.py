#/==================================================================\#
#                                                                    #
#\==================================================================/#

#\==================================================================/#
#/========================/ installed libs \========================\#  

import traceback, \
         schedule, \
           telebot, \
               time, \
                  io

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
                ).row(           pin[5], pin[6]
            )
        return markup
    except:
        saveLogs(f'[markupMaker]---->{traceback.format_exc()}')

    return types.ReplyKeyboardMarkup(resize_keyboard=True)
#\==================================================================/#


#\==================================================================/#
from dotenv import load_dotenv
import os
load_dotenv('./setup/.env')
bot = telebot.TeleBot(os.getenv('TOKEN'))
#\==================================================================/#


#\==================================================================/#
class P_schedule:
    """
    This class reposts messages from the telegram channel.
    """

    def start_schedule():
        schedule.every(30).minutes.do(P_schedule.send_post)
        while True:
            schedule.run_pending()
            time.sleep(1)


    def send_post():
        
        def get_time():
            return int(time.time())
        
        cex = 0; msg_id = dbMessageId('take_id')[0][0]
        accs = get_accounts()
        
        for ind in accs.keys():
            try:
                if (get_time() - accs[ind].timer_conv > 900) and accs[ind].conversation == 'open':
                    stopConversation(msg=None, lang=0 if isRu(accs, None, int(ind)) else 1, _id=ind)
            except: 
                pass
            try:
                bot.forward_message(int(ind), CHANNEL_ID, msg_id)
                time.sleep(1)
            except:
                cex+=1
        if cex == len(accs): 
            cex = 0
        else:
            try:
                bot.forward_message(281321076, CHANNEL_ID, msg_id)
                dbMessageId('save_id', msg_id+1)
            except:
                pass
#\==================================================================/#


#\==================================================================/#
@bot.message_handler(commands=['start'])
def welcome(msg):
    global accounts

    _id = str(msg.chat.id)

    accounts = get_accounts()

    _accounts = [_id]

    if len(msg.html_text.split()) > 1 and msg.html_text.split()[1].isdigit():
        run_id = msg.html_text.split()[1]
    else:
        run_id = None
    
    if _id in accounts.keys():
        acc = accounts[_id]
        acc.link_enter = run_id
        update_account(accounts[str(_id)], 'link_enter', run_id)
        if not acc.language:
            inlineMessages(
                markup_text = "🔱Choose language", 
                msg         = msg, 
                markup_arr  = [["Русский", "Русский"], 
                               ["Ozbek", "Ozbek"]], 
                action      = False
            )
        elif acc.personal_data == 'YES':
            bot.send_message(msg.chat.id,
                f'{EMJ_DOCTOR}Вы уже зарегистрированы в системе!'
                if isRu(accounts, msg = msg) else
                "🔱Siz allaqachon ro'yxatdan o'tgansiz!"
            )
            
            if acc.link_enter and acc.link_enter.isdigit() and not checkOperId(str(_id), 'all_ids_arr'):
                key : Dict = message_text_dict[f'{EMJ_RAISING_HAND} Оператор']
                update_account(acc, 'link_enter', None)
                operInit(msg, accounts, [acc.link_enter], [acc.link_enter])
            else:
                keyboardRefMaker(msg, not isRu(accounts, msg = msg))
            
        elif acc.personal_data == 'NO':
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
        _accounts += [msg.chat.username, msg.chat.first_name, [], 'close', '0', [], '0', 'NO', None, 'close', 0, run_id]
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
    for oper_id in action_oper_select[_oper] if isinstance(_oper, str) else _oper:
        try:
            bot.send_message(int(oper_id), 
               op_txt, reply_markup=markup
            )
        
        except telebot.apihelper.ApiException:
            continue
        
        except:
            saveLogs(f'[sendReqtoOper]---->{traceback.format_exc()}')
        
def operKeyboardMaker(msg, which_oper, lang, u_id = None) -> None:
    global accounts

    _id : str = u_id if u_id else str(msg.chat.id)
    
    f_name = accounts[_id].name
    u_name = accounts[_id].login

    try:
        accounts[_id].conversation = 'mid'

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

        insert_message(int(_id), 0)

        sendReqtoOper(which_oper, 
            f'-------Запрос переписки!------- \n'
            f'id:        {_id}                \n'
            f'Имя:       {f_name}             \n'
            f'Username: @{u_name}             \n'
            f'Язык: Русский                   \n'
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
    id_text = False
    try:
        int(msg.text); id_text = get_text(msg.text, mod)
    except:
        pass
    bot.send_message(msg.chat.id, 
        id_text if id_text else 'Такого номера нет в базе!'
    )

def pushingLabelFromFile(msg, _accs, path1, path2) -> None:
    bot.send_message(msg.chat.id, 
        openfileforRead(None, path1 if isRu(_accs, msg = msg) else path2)
    )

def operInit(msg, accs, action, set_act, u_id = None):
    try:
        if checkOperId(str(msg.chat.id), action):
            bot.send_message(msg.chat.id, "Вы оператор!")
        else:
            operKeyboardMaker(msg, set_act, 
                0 if isRu(accs, msg) else 1, u_id)
    except:
        saveLogs(f'[operInit]---->{traceback.format_exc()}')
        work_msg(msg.chat.id)
        
def redirectInit(msg, action) -> None:
    global accounts

    _id : str = str(msg.chat.id)
    
    try:
        bot.send_message(_id, action)

        if len(accounts[_id].tags) != 0:

            _tag : str = accounts[_id].tags[0]

            bot.send_message(str(_tag), action)

            tag : str = accounts[_tag]

            update_account(tag, 'conversation', 'close')
            update_account(tag, 'tags', [])        
            accounts = get_accounts()

            keyboardRefMaker(msg, 
                0 if isRu(accounts, msg) else 1, _tag
            )

        keyboardRefMaker(msg, 0)
        inlineMessages(
            markup_text = 'Оцените работу оператора!' 
                if isRu(accounts, msg) else 
                'Operator ishini baholang!', 
            _id = accounts[_id].tags[0] 
                if checkOperId(_id, all_ids_arr) else _id, 
            markup_arr = [["👍", "👍"], 
                          ["👎", "👎"]], 
            action = False
        )
    except:
        saveLogs(f'[redirectInit]---->{traceback.format_exc()}')
        bot.send_message(_id, 'Forwarding error!')

   
def stopConversation(msg, lang, _id = None, action = None) -> None:
    global accounts

    u_id : str = _id if _id != None else str(msg.chat.id)

    push_text = f"{EMJ_EXCLAMATION} Завершение диалога" \
                if lang == 0 or lang == 'Русский' else  \
                f"{EMJ_EXCLAMATION} Muloqotni yakunlash"

    bot.send_message(u_id, push_text)

    acc : Account = accounts[u_id]

    if len(acc.tags):

        t_id : str = acc.tags[0]

        try:
            bot.send_message(t_id, push_text)
        except:
            pass

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

    change_status(msg.chat.id)
            
    update_account(acc, 'conversation', 'close')
    update_account(acc, 'tags', [])

    accounts = get_accounts()

def closeConversation(msg):
    global accounts

    try:
        acc = accounts[str(msg.chat.id)]
            
        update_account(acc, 'conversation', 'close')
        update_account(acc, 'tags', [])        
        accounts = get_accounts()
            
        change_status(msg.chat.id)
    except:
        saveLogs(f'[closeConversation]---->{traceback.format_exc()}')
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

                if key[0] == 'text_show': 
                    pushingLabelFromFile(msg, accounts, key[1], key[2])

                elif key[0] == 'oper_show': 
                    operInit(msg, accounts, key[1], key[2])

                elif key[0] == 'oper_close': 
                    stopConversation(msg, key[1])

                elif key[0] == 'redirect':
                    redirectInit(msg,
                        f"{EMJ_EXCLAMATION} Общение завершено, перенаправление {key[1]}"
                    )
                    operInit(msg, accounts, key[3], key[3], acc.tags[0])
                    closeConversation(msg)

            elif txt == f'{EMJ_BACK_ARROW} Назад': 
                keyboardRefMaker(msg, acc.language)

            elif txt in (f'{EMJ_EXCLAMATION} Оставить жалобу', 
                         f'{EMJ_EXCLAMATION} Shikoyat qoldiring'):
                work_msg(msg.chat.id)

            elif txt == f"{EMJ_MONEY_BAG} Инкассация":
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

            elif txt in (f'{EMJ_PLUS} Мой ID', f'{EMJ_PLUS} Mening ID'):
                id_txt = "Ваш ID:" if isRu(accounts, id = _id) else "Sizning ID:"
                bot.send_message(_id, f'{EMJ_NOTE} {id_txt} {_id}')

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
                update_account(accounts[str(_id)], 'link_enter', None)
                bot.send_message(_id, _key[1])
            elif _key[0] == 'agree_data':
                if update_account(accounts[str(_id)], 'personal_data', 'YES'):

                    accounts = get_accounts()

                    del_msg(_id, m_id)
                    
                    if accounts[str(_id)].link_enter and accounts[str(_id)].link_enter.isdigit() and not checkOperId(str(_id), 'all_ids_arr'):
                        key : Dict = message_text_dict[f'{EMJ_RAISING_HAND} Оператор']
                        update_account(accounts[str(_id)], 'link_enter', None)
                        operInit(call.message, accounts, [accounts[str(_id)].link_enter], [accounts[str(_id)].link_enter])
                    else:
                        keyboardRefMaker(call.message, 
                            accounts[str(_id)].language
                        )
                else:
                    work_msg(_id)
            elif _key[0] in ('no_code', 'has_code'):
                del_msg(_id, m_id)
                keyboardRefMaker(call.message, 
                    accounts[str(_id)].language
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
        
        elif _data == '👍' or _data == '👎':
            del_msg(_id, m_id)
            bot.send_message(_id, 
                'Спасибо за оценку!' 
                if isRu(accounts, id = _id) else 
                'Baholash uchun rahmat!'
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
                        markup = markupMaker('redirect', buttons_oper_text)
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
                            f"{EMJ_TELEPHONE} Найден оператор #{_id}, "
                            "переписка активирована" 
                            if isRu(accounts, id = u_id) else 
                            f"{EMJ_TELEPHONE} Operator #{_id} topildi, "
                            "yozishmalar faollashtirildi"
                        )
                        
                        bot.send_message(_id, 
                            f"{EMJ_TELEPHONE} Вы подтвердили заявку!",
                            reply_markup=markup
                        )
                        db_answer = insert_message(u_id, _id)

                        bot.send_message(u_id, db_answer)
                        bot.send_message( _id, db_answer)

                        break

                if accounts[str(_id)].conversation != 'open':
                    if accounts[str(_data)].conversation != 'open':
                        bot.send_message(_id, 
                            f"Пользователь id: {_data} отменил режим!\n"
                            "Повторный вызов..."
                        )
                        
                        markup = markupMaker('redirect', buttons_oper_text)
                        user_markup = markupMaker('person', buttons_oper_text 
                            if isRu(accounts, id = str(_data)) else buttons_user_uz_text
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
                            if isRu(accounts, id = str(_data)): 
                                bot.send_message(_data, 
                                    f"{EMJ_TELEPHONE} Оператор"
                                    f" #{str(_id)} активировал переписку", 
                                    reply_markup=user_markup
                                )
                            else: 
                                bot.send_message(_data, 
                                    f"{EMJ_TELEPHONE} Operator #{str(_id)} "
                                    "yozishmalarni faollashtirdi", 
                                    reply_markup=user_markup
                                )

                            bot.send_message(_id, 
                                f"{EMJ_TELEPHONE} Вы подтвердили заявку!", 
                                reply_markup=markup
                            )
                            db_answer = insert_message(_data, _id)

                            bot.send_message(_data, db_answer)
                            bot.send_message(  _id, db_answer)
                        except:
                            update_account(
                                accounts[str(_id)], 
                                'conversation', 
                                'close'
                            )
                            update_account(
                                accounts[str(_data)], 
                                'conversation', 
                                'close'
                            )
                            update_account(accounts[str(_data)], 'tags', [])
                            update_account(accounts[str(  _id)], 'tags', [])

                            accounts = get_accounts()

                            bot.send_message(_id, 'Пользователь выключил бота!')
                    else:
                        bot.send_message(_id, 
                            "Другой оператор отвечает на заявку!"
                        )
            else:
                bot.send_message(_id, 
                    "Закончите старый диалог, чтобы начать новый!"
                )


    except:
        saveLogs(f"[call]---->{traceback.format_exc()}\n]")
#\==================================================================/#


#\==================================================================/#
if __name__ == '__main__':
    proc = Process(target = P_schedule.start_schedule, args = ())
    proc.start()
    try: 
        bot.polling(none_stop=True)

    except OSError:
        bot.send_message(281321076, [OSError])
        proc.kill()

    except:
        saveLogs(f"Program error!\n\n{traceback.format_exc()}")

        bot.send_message(281321076, 'Program error!')
#\==================================================================/#
