import schedule
import datetime
import psycopg2
import telebot
import config
import time
import json
import io
import os
from PIL import Image, ImageFilter, ImageFilter, ImageDraw, ImageFont
from multiprocessing import *
from telebot import types

path_acc_settings = "settings/account_settings.txt" 
path_feedbacks = "settings/feedbacks.txt" 


path_first_lang = "first_language/fl_start_label.txt"
path_FAQ_label = "first_language/fl_FAQ_label.txt"
path_telephone_num = "first_language/fl_telephone_num_label.txt"
path_address_label = "first_language/fl_address_label.txt"
path_oper_label = "first_language/fl_oper_label.txt"
path_FAQoper_label = "first_language/fl_FAQoper_label.txt"
path_recv_label = "first_language/fl_recv_label.txt"
path_order_label = "first_language/fl_order_label.txt"
path_discount_label = "first_language/fl_discount_label.txt"
path_social_web = "first_language/fl_social_web.txt"

path_second_lang = "second_language/sl_start_label.txt"
path_sec_FAQ_label = "second_language/sl_FAQ_label.txt"
path_sec_telephone_num = "second_language/sl_telephone_num_label.txt"
path_sec_address_label = "second_language/sl_address_label.txt"
path_sec_oper_label = "second_language/sl_oper_label.txt"
path_sec_FAQoper_label = "second_language/sl_FAQoper_label.txt"
path_sec_recv_label = "second_language/sl_recv_label.txt"
path_sec_order_label = "second_language/sl_order_label.txt"
path_sec_discount_label = "second_language/sl_discount_label.txt"
path_sec_social_web = "second_language/sl_social_web.txt"

MESSAGE_ID = 254
BOT_ID = 1364784224
CHANAL_ID = -1001229753165

account_settings = {}
feed_back = {}
new_acc_id = ""
txt = ""
mess = ""
with open(path_acc_settings, 'r') as file_set:
    if(file_set.readline() == ""): account_settings = {}
    else:
        file_set.close()
        with open(path_acc_settings, 'r') as file_set:
            account_settings = json.load(file_set)

bot = telebot.TeleBot(config.TOKEN)

def connect():
    try:
        con = psycopg2.connect(database="postgres",user="postgres",password="postgres", host="127.0.0.1",port="5432")
        cur = con.cursor()
        return con, cur
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Error while connecting PostgreSQL!", error)
        return 0

def insert_new_data(user_id, oper_id):
    con, cur = connect()
    if con == 0 and cur == 0:
        return 0
    else:
        try:
            if oper_id == '0':
                dt = datetime.date.today()
                tt = dt.timetuple()
                date_start = ''
                ch_i = 0
                for it in tt:
                    date_start += str(it)
                    ch_i += 1
                    if ch_i >= 3: break
                    else: date_start += '-'
                txt_db_com = "INSERT INTO message_tb (user_id, oper_id, date_start, text, status) VALUES (" + user_id + ', ' + oper_id + ", '" + date_start + "', 'TEXT DATABASE', 'open')"
                cur.execute(txt_db_com)
                con.commit()
                print('New data add!')
                return 1
            elif user_id != '0' and oper_id != '0':
                txt_db_com = "UPDATE message_tb SET oper_id = " + oper_id + ", text = '" + "TEXT DATABASE\nOperator: " + oper_id + "\nUser: " + user_id + "\n'" + " WHERE status = 'open' AND user_id = " + user_id
                cur.execute(txt_db_com)
                con.commit()
                print('New data add!')
                txt_db_com = "SELECT id FROM message_tb WHERE status = 'open' and user_id = " + user_id
                cur.execute(txt_db_com)
                ed_text = cur.fetchall()
                text_adder = ed_text[0]
                text_adder = '✏️id Переписки: ' + str(text_adder[0])
                bot.send_message(int(oper_id), text_adder)
                bot.send_message(int(user_id), text_adder)
                return 1
        except Exception as e:
            print('Error entering new data to message_tb!', e)
            return 0
def insert_new_feedback_data(oper_id, user_id, txt):
    con, cur = connect()
    if con == 0 and cur == 0:
        return 0
    else:
        try:
            if oper_id == '0' and user_id != '0':
                dt = datetime.date.today()
                tt = dt.timetuple()
                date_enter = ''
                ch_i = 0
                for it in tt:
                    date_enter += str(it)
                    ch_i += 1
                    if ch_i >= 3: break
                    else: date_enter += '-'
                txt_db_com = "INSERT INTO feedback_tb (user_id, oper_id, date_enter, text_fb, status) VALUES (" + user_id + ', ' + oper_id + ", '" + date_enter + "', '" + txt +"', 'open')"
                cur.execute(txt_db_com)
                con.commit()
                print('New data add!')
                txt_db_com = "SELECT id FROM feedback_tb WHERE status = 'open' and user_id = " + user_id
                cur.execute(txt_db_com)
                ed_text = cur.fetchall()
                text_adder = ed_text[0]
                text_adder = '✏️id Жалобы: ' + str(text_adder[0])
                bot.send_message(int(user_id), text_adder)
                return 1
            else:
                txt_db_com = "SELECT text_fb FROM feedback_tb WHERE status = 'open' and user_id = " + user_id
                cur.execute(txt_db_com)
                ed_text = cur.fetchall() 
                text_adder = ed_text[0]
                text_adder = text_adder[0] + '\n' + "Operator: " + oper_id + '\nТекст: ' + txt
                txt_db_com = "UPDATE feedback_tb SET oper_id = " + oper_id + ", text_fb = '" + "TEXT FEEDBACK\n" + text_adder + "'" + " WHERE status = 'open' AND user_id = " + user_id
                cur.execute(txt_db_com)
                con.commit()
                print('New data add!')
                txt_db_com = "SELECT id FROM feedback_tb WHERE status = 'open' and user_id = " + user_id
                cur.execute(txt_db_com)
                ed_text = cur.fetchall()
                text_adder = ed_text[0]
                text_adder = '✏️id Жалобы: ' + str(text_adder[0])
                bot.send_message(int(oper_id), text_adder)
                #bot.send_message(int(user_id), text_adder)
                txt_db_com = "UPDATE feedback_tb SET status = 'close' WHERE status = 'open' AND user_id = " + user_id
                cur.execute(txt_db_com)
                con.commit()
                return 1
        except Exception as e:
            print('Error entering new data to feedback_tb!', e)
            return 0

def insert_text_to_data(text_val, sm_id):
    con, cur = connect()
    if con == 0 and cur == 0:
        return 0
    else:
        try:
            txt_db_com = "SELECT text FROM message_tb WHERE status = 'open' and (oper_id = " + sm_id + ' or user_id = ' + sm_id + ')'
            cur.execute(txt_db_com)
            ed_text = cur.fetchall() 
            text_adder = ed_text[0]
            text_adder = text_adder[0] + '\n' + text_val
            txt_db_com = "UPDATE message_tb SET text = '" + text_adder + "' WHERE status = 'open' and (user_id = " + sm_id + ' or oper_id = ' + sm_id + ')'
            cur.execute(txt_db_com)
            con.commit()
            return 1
        except Exception as e:
            print('Error entering data to message_tb!', e)
            return 0

def closerDataBase(sm_id):
    con, cur = connect()
    if con == 0 and cur == 0:
        return 0
    else:
        try:
            txt_db_com = "SELECT user_id, oper_id FROM message_tb WHERE status = 'open' and (oper_id = " + sm_id + ' or user_id = ' + sm_id + ')'
            cur.execute(txt_db_com)
            ed_text = cur.fetchall()
            if ed_text[0][0] == 0 or ed_text[0][1] == 0:
                txt_db_com = "delete from message_tb where status = 'open' and (oper_id = " + sm_id + ' or user_id = ' + sm_id + ')'
                cur.execute(txt_db_com)
            else:
                txt_db_com = "UPDATE message_tb SET status = 'close' WHERE status = 'open' and user_id = " + sm_id + ' or oper_id = ' + sm_id
                cur.execute(txt_db_com)
            con.commit()
            return 1
        except Exception as e:
            print('Error entering data to message_tb!', e)
            return 0

def getDataFromDB(date_start):
    con, cur = connect()
    if con == 0 and cur == 0:
        return 0
    else:
        try:
            txt_db_com = "SELECT id, user_id FROM message_tb WHERE date_start = '" + date_start + "'"
            cur.execute(txt_db_com)
            ed_text = cur.fetchall()
            text_adder = 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n'
            for i in ed_text:
                for k in account_settings:
                    if k == str(i[1]):
                        if account_settings[k]['login'] != 'None':
                            name_id = '@' + account_settings[k]['login']
                        else: name_id = account_settings[k]['name']
                        break
                text_adder = text_adder + str(i[0]) + ') ' + 'Name: ' + name_id + ' --- Id: ' + str(i[1]) + '\n'
            con.commit()
            if text_adder == 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n': return '0' 
            else: return text_adder
        except Exception as e:
            print('Error data message_tb!', e)
            return '0'
def getDataFromFeedBackDB(date_start):
    con, cur = connect()
    if con == 0 and cur == 0:
        return 0
    else:
        try:
            txt_db_com = "SELECT id, user_id FROM feedback_tb WHERE date_enter = '" + date_start + "'"
            cur.execute(txt_db_com)
            ed_text = cur.fetchall()
            text_adder = 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n'
            for i in ed_text:
                for k in account_settings:
                    if k == str(i[1]):
                        if account_settings[k]['login'] != 'None':
                            name_id = '@' + account_settings[k]['login']
                        else: name_id = account_settings[k]['name']
                        break
                text_adder = text_adder + str(i[0]) + ') ' + 'Name: ' + name_id + ' --- Id: ' + str(i[1]) + '\n'
            con.commit()
            if text_adder == 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n': return '0' 
            else: return text_adder
        except Exception as e:
            print('Error data feedback_tb!', e)
            return '0'

def getTextFromDB(id_text):
    con, cur = connect()
    if con == 0 and cur == 0:
        return 0
    else:
        try:
            txt_db_com = "SELECT text FROM message_tb WHERE id = " + id_text
            cur.execute(txt_db_com)
            ed_text = cur.fetchall()
            text_taker = ed_text[0]
            text_taker = text_taker[0]
            con.commit()
            return text_taker
        except Exception as e:
            print('Error, wrong id!', e)
            return '0'
def getTextFromFeedBackDB(id_text):
    con, cur = connect()
    if con == 0 and cur == 0:
        return 0
    else:
        try:
            txt_db_com = "SELECT text_fb FROM feedback_tb WHERE id = " + id_text
            cur.execute(txt_db_com)
            ed_text = cur.fetchall()
            text_taker = ed_text[0]
            text_taker = text_taker[0]
            con.commit()
            return text_taker
        except Exception as e:
            print('Error, wrong id!', e)
            return '0'

def change_data(name):
    con, cur = connect()
    if con == 0 or cur == 0:
        return 0
    else:
        try:
            txt_data_del = "UPDATE user_tb set phone = NULL where name = '" + name + "'"
            cur.execute(txt_data_del)  
            con.commit()   
        except Exception as e:
            err_txt = 'Error deleting data from user @' + name + '!'
            print(err_txt, e)


def start_process():#Запуск Process
    p1 = Process(target=P_schedule.start_schedule, args=()).start()
class P_schedule(): # Class для работы c schedule
    def start_schedule(): #Запуск schedule
        ######Параметры для schedule######
        schedule.every(30).seconds.do(P_schedule.send_post)
        ##################################
        
        while True: #Запуск цикла
            schedule.run_pending()
            time.sleep(1)
 
    ####Функции для выполнения заданий по времени  
    def send_post():
        global MESSAGE_ID
        global CHANAL_ID
        global BOT_ID
        global account_settings
        c_ex = 0
        #try:
        with open(path_acc_settings, 'r') as file_set:
            if(file_set.readline() == ""): account_settings = {}
            else:
                file_set.close()
                with open(path_acc_settings, 'r') as file_set:
                    account_settings = json.load(file_set)
        for i in account_settings.keys():
            try:
                bot.forward_message(int(i), -1001229753165, MESSAGE_ID)
            except Exception as ex:
                c_ex+=1
                #print(repr(ex))
                continue
        if c_ex == len(account_settings):
            c_ex = 0
        else:
            try:
                bot.forward_message(281321076, -1001229753165, MESSAGE_ID)
                MESSAGE_ID += 1
            except Exception as qt:
                print(repr(qt))
        #except Exception as e:
            #print(repr(e))


@bot.message_handler(commands=['start'])
def welcome(message):
    global account_settings
    global new_acc_id
    with open(path_acc_settings, 'r') as file_set:
        if(file_set.readline() == ""): account_settings = {}
        else:
            file_set.close()
            with open(path_acc_settings, 'r') as file_set:
                account_settings = json.load(file_set)
    new_acc_id = str(message.chat.id)
    checker_keys = account_settings.setdefault(new_acc_id)
    if checker_keys == None or account_settings[new_acc_id]["language"] == None:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Русский", callback_data='Русский')
        item2 = types.InlineKeyboardButton("Ozbek", callback_data="Ozbek")
        markup.add(item1, item2)

        account_settings[new_acc_id] = {"login" : str(message.chat.username), "name" : str(message.chat.first_name), "oper_ids" : [], "conversation" : "close", "discount" : "0", "tags" : [], "ref" : "0", "personal data" : "NO", "language" : None, "feedback_st" : 'close'}
        with open(path_acc_settings, 'w+') as f:
            json.dump(account_settings, f, indent='    ')
        with open(path_acc_settings, 'r') as fle:
            account_settings = json.load(fle)

        bot.send_message(message.chat.id,"🔱Choose language", reply_markup=markup)
    else:
        if account_settings[new_acc_id]["language"] == "Русский":
            if account_settings[new_acc_id]["personal data"] == "YES": 
                bot.send_message(message.chat.id,"🔱Вы уже зарегистрированы в системе!")
                keyboardRefMaker(message)
            elif account_settings[new_acc_id]["personal data"] == "NO":
                with io.open(path_first_lang, encoding='utf-8') as start_text_file:
                    start_txt = ""
                    for i in start_text_file:
                        start_txt += i
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Согласен", callback_data='Согласен')
                item2 = types.InlineKeyboardButton("Отказываюсь", callback_data='Отказываюсь')
                markup.add(item1, item2)
                bot.send_message(message.chat.id, start_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        else: 
            if account_settings[new_acc_id]["personal data"] == "YES": 
                bot.send_message(message.chat.id,"🔱Siz allaqachon ro'yxatdan o'tgansiz!")
                keyboardRefMakerSec(message)
            elif account_settings[new_acc_id]["personal data"] == "NO":
                with io.open(path_second_lang, encoding='utf-8') as start_text_file:
                    start_txt = ""
                    for i in start_text_file:
                        start_txt += i
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("ROZIMAN", callback_data='Agree')
                item2 = types.InlineKeyboardButton("Qo'shilmayman", callback_data='Disagree')
                markup.add(item1, item2)
                bot.send_message(message.chat.id, start_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['changeLabel'])
def adderNewLabel(message):
    if(message.chat.id == 667068180):
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


def operKeyboardMaker(message):
    global account_settings
    account_settings[str(message.chat.id)]["conversation"] = 'mid'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🔙 Отклонить вызов оператора")
    item2 = types.KeyboardButton("❔ Инструкция")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "🙋 Включён режим переписки с оператором", reply_markup=markup)
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
    insert_new_data(user_id, oper_id)
    bot.send_message(281321076, oper_send_text, reply_markup=markup)
    bot.send_message(667068180, oper_send_text, reply_markup=markup)

def dirKeyboardMaker(message):
    global account_settings
    account_settings[str(message.chat.id)]["conversation"] = 'mid'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🔙 Отклонить вызов оператора")
    item2 = types.KeyboardButton("❔ Инструкция")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "🙋 Включён режим переписки с оператором", reply_markup=markup)
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
    insert_new_data(user_id, oper_id)
    bot.send_message(281321076, oper_send_text, reply_markup=markup)
    #bot.send_message(667068180, oper_send_text, reply_markup=markup)
    bot.send_message(907508218, oper_send_text, reply_markup=markup)

def operKeyboardMakerSec(message):
    global account_settings
    account_settings[str(message.chat.id)]["conversation"] = 'mid'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
    oper_send_text += "\nЯзык: Ozbek\n----------------------------"
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Принять", callback_data=str(message.chat.id))
    markup.add(item1)
    user_id = str(message.chat.id)
    oper_id = '0'
    insert_new_data(user_id, oper_id)
    bot.send_message(281321076, oper_send_text, reply_markup=markup)
    bot.send_message(667068180, oper_send_text, reply_markup=markup)

def dirKeyboardMakerSec(message):
    global account_settings
    account_settings[str(message.chat.id)]["conversation"] = 'mid'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
    oper_send_text += "\nЯзык: Ozbek\n----------------------------"
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Принять", callback_data=str(message.chat.id))
    markup.add(item1)
    user_id = str(message.chat.id)
    oper_id = '0'
    insert_new_data(user_id, oper_id)
    bot.send_message(281321076, oper_send_text, reply_markup=markup)
    #bot.send_message(667068180, oper_send_text, reply_markup=markup)
    bot.send_message(907508218, oper_send_text, reply_markup=markup)


def dbDateSortEnter(message):
    send = bot.send_message(message.chat.id, '➕ Введите дату в формате ГОД-МЕСЯЦ-ДЕНЬ (2000-1-12)')
    bot.register_next_step_handler(send, dbSortEnter)
def feedBackdbDateSortEnter(message):
    send = bot.send_message(message.chat.id, '➕ Введите дату в формате ГОД-МЕСЯЦ-ДЕНЬ (2000-1-12)')
    bot.register_next_step_handler(send, FeedBackdbSortEnter)


def dbSortEnter(message):
    date_text = message.text
    date_text = getDataFromDB(date_text)
    if date_text == '0': 
        bot.send_message(message.chat.id, 'Данной даты нет в базе!')
        return
    else: bot.send_message(message.chat.id, date_text)
    send = bot.send_message(message.chat.id, '➕ Введите номер строки по нужному имени или id')
    bot.register_next_step_handler(send, dbIdSortEnter)
def FeedBackdbSortEnter(message):
    date_text = message.text
    date_text = getDataFromFeedBackDB(date_text)
    if date_text == '0': 
        bot.send_message(message.chat.id, 'Данной даты нет в базе!')
        return
    else: bot.send_message(message.chat.id, date_text)
    send = bot.send_message(message.chat.id, '➕ Введите номер строки по нужному имени или id')
    bot.register_next_step_handler(send, FeedBackdbIdSortEnter)

def dbIdSortEnter(message):
    id_text = message.text
    id_text = getTextFromDB(id_text)
    if id_text == '0':
        bot.send_message(message.chat.id, 'Такого номера нет в базе!')
        return
    else: bot.send_message(message.chat.id, id_text)
def FeedBackdbIdSortEnter(message):
    id_text = message.text
    id_text = getTextFromFeedBackDB(id_text)
    if id_text == '0':
        bot.send_message(message.chat.id, 'Такого номера нет в базе!')
        return
    else: bot.send_message(message.chat.id, id_text)


@bot.message_handler(content_types=['text', 'photo'])
def lol(message):
    global account_settings
    global mess
    global feed_back
    if message.chat.type == 'private':
        if message.text == '📞 Телефон' or message.text == '📞 telefon':
            telephone_num = ""
            if account_settings[str(message.chat.id)]["language"] == "Русский":
                with io.open(path_telephone_num, encoding='utf-8') as file_set:
                    for i in file_set:
                        telephone_num += i
            else:
                with io.open(path_sec_telephone_num, encoding='utf-8') as file_set:
                    for i in file_set:
                        telephone_num += i
            bot.send_message(message.chat.id, telephone_num.format(message.chat, bot.get_me()),parse_mode='html')
        elif message.text == '🏠 Адреса' or message.text == '🏠 manzillari':
            address = ""
            if account_settings[str(message.chat.id)]["language"] == "Русский":
                with io.open(path_address_label, encoding='utf-8') as file_set:
                    for i in file_set:
                        address += i
            else:
                with io.open(path_sec_address_label, encoding='utf-8') as file_set:
                    for i in file_set:
                        address += i
            bot.send_message(message.chat.id, address.format(message.chat, bot.get_me()),parse_mode='html')
        elif message.text == '🙋 Оператор' or message.text == '🙋 Operator':
            if message.chat.id != 281321076 and message.chat.id != 667068180:
                if account_settings[str(message.chat.id)]["language"] == "Русский":
                    operKeyboardMaker(message)
                else:
                    operKeyboardMakerSec(message)
            else:
                bot.send_message(message.chat.id, "Вы оператор!")
        elif message.text == '✍️ Написать директору' or message.text == '✍️ Direktorga yozing':
            if message.chat.id != 281321076 and message.chat.id != 667068180 and message.chat.id != 907508218:
                if account_settings[str(message.chat.id)]["language"] == "Русский":
                    dirKeyboardMaker(message)
                else:
                    dirKeyboardMakerSec(message)
            else:
                bot.send_message(message.chat.id, "Вы оператор!")
        elif message.text == '📝 Создать заказ' or message.text == '📝 buyurtma yaratish':
            oper_write = ""
            if account_settings[str(message.chat.id)]["language"] == "Русский":
                with io.open(path_order_label, encoding='utf-8') as file_set:
                    for i in file_set:
                        oper_write += i
            else:
                with io.open(path_sec_order_label, encoding='utf-8') as file_set:
                    for i in file_set:
                        oper_write += i
            bot.send_message(message.chat.id, oper_write.format(message.chat, bot.get_me()),parse_mode='html')
        elif message.text == '❗️ Оставить жалобу' or message.text == '❗️ Shikoyat qoldiring':
            if message.chat.id != 281321076 and message.chat.id != 667068180 and message.chat.id != 263305395 and message.chat.id != 666803198 and message.chat.id != 907508218:
                oper_write = ""
                account_settings[str(message.chat.id)]["feedback_st"] = 'open'
                markup = types.InlineKeyboardMarkup(row_width=2)
                if account_settings[str(message.chat.id)]["language"] == "Русский":
                    with io.open(path_recv_label, encoding='utf-8') as file_set:
                        for i in file_set:
                            oper_write += i
                    item1 = types.InlineKeyboardButton("Написать жалобу", callback_data='Написать жалобу')
                else:
                    with io.open(path_sec_recv_label, encoding='utf-8') as file_set:
                        for i in file_set:
                            oper_write += i
                    item1 = types.InlineKeyboardButton("Shikoyat yozing", callback_data='Write a feedback')
                markup.add(item1)
                account_settings[str(message.chat.id)]["feedback_st"] = 'open'
                bot.send_message(message.chat.id, oper_write.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            else:
                feedBackdbDateSortEnter(message)
        elif message.text == '💽 БД переписок' or message.text == '💽 Yozishmalar bazasi':
            if message.chat.id == 281321076 or message.chat.id == 667068180 or message.chat.id == 263305395 or message.chat.id == 666803198 or message.chat.id == 907508218:
                dbDateSortEnter(message)
            else:
                if account_settings[str(message.chat.id)]["language"] == "Русский":
                    bot.send_message(message.chat.id, 'У вас нет прав для чтения базы!')
                else: bot.send_message(message.chat.id, "Sizda bazani o'qish huquqi yo'q!")
        elif message.text == '% Получить скидку' or message.text == '% Chegirma oling':
            oper_write = ""
            mess = "new"
            if (account_settings[str(message.chat.id)]["discount"] == "0" and account_settings[str(message.chat.id)]["ref"] == "0"):
                markup = types.InlineKeyboardMarkup(row_width=2)
                if account_settings[str(message.chat.id)]["language"] == "Русский":
                    with io.open(path_discount_label, encoding='utf-8') as file_set:
                        for i in file_set:
                            oper_write += i
                    oper_write += "\nВаш реферальный код: "
                    oper_write += str(message.chat.id)
                    bot.send_message(message.chat.id, oper_write.format(message.chat, bot.get_me()),parse_mode='html')
                else:
                    with io.open(path_sec_discount_label, encoding='utf-8') as file_set:
                        for i in file_set:
                            oper_write += i
                    oper_write += "\nSizning tavsiyangiz kodi: "
                    oper_write += str(message.chat.id)
                    bot.send_message(message.chat.id, oper_write.format(message.chat, bot.get_me()),parse_mode='html')
            elif account_settings[str(message.chat.id)]["ref"] == "10":
                account_settings[str(message.chat.id)]["discount"] = "10"
                with open(path_acc_settings, 'w+') as f:
                    json.dump(account_settings, f, indent='    ')
                with open(path_acc_settings, 'r') as fle:
                    account_settings = json.load(fle)
                if account_settings[str(message.chat.id)]["language"] == "Русский":
                    picPNGmaker(message)
                    bot.send_message(message.chat.id, "✅ У вас максимальная скидка!")
                else:
                    picPNGmaker(message)
                    bot.send_message(message.chat.id, "✅ Siz maksimal chegirma bor!")
            else:
                if account_settings[str(message.chat.id)]["language"] == "Русский":
                    if account_settings[str(message.chat.id)]["discount"] == "10":
                        picPNGmaker(message)
                        bot.send_message(message.chat.id, "✅ У вас максимальная скидка!")
                    else:
                        text_tags = "❌ Ваши друзья ещё не активировали бота!\n❌ Всего активаций "
                        text_tags += account_settings[str(message.chat.id)]["ref"]
                        text_tags += " из 10"
                        bot.send_message(message.chat.id, text_tags)
                        picPNGmaker(message)
                else:
                    if account_settings[str(message.chat.id)]["discount"] == "10":
                        picPNGmaker(message)
                        bot.send_message(message.chat.id, "✅ Siz maksimal chegirma bor!")
                    else:
                        text_tags = "❌ Sizning do'stlaringiz hali botni faollashtirmagan!\n❌ Jami aktivatsiyalar "
                        text_tags += account_settings[str(message.chat.id)]["ref"]
                        text_tags += " dan 10"
                        bot.send_message(message.chat.id, text_tags)
                        picPNGmaker(message)
        elif message.text == '®FAQ Инструкция' or message.text == "®FAQ Ko'rsatma":
            FAQ_txt = ""
            if account_settings[str(message.chat.id)]["language"] == "Русский":
                with io.open(path_FAQ_label, encoding='utf-8') as file_set:
                    for i in file_set:
                        FAQ_txt += i
            else:
                with io.open(path_sec_FAQ_label, encoding='utf-8') as file_set:
                    for i in file_set:
                        FAQ_txt += i
            bot.send_message(message.chat.id, FAQ_txt.format(message.chat, bot.get_me()),parse_mode='html')
        elif message.text == '🌐 Мы в социальных сетях' or message.text == '🌐 Biz ijtimoiy tarmoqlarda':
            soc_web = ""
            if account_settings[str(message.chat.id)]["language"] == "Русский":
                with io.open(path_social_web, encoding='utf-8') as file_set:
                    for i in file_set:
                        soc_web += i
            else:
                with io.open(path_sec_social_web, encoding='utf-8') as file_set:
                    for i in file_set:
                        soc_web += i
            bot.send_message(message.chat.id, soc_web.format(message.chat, bot.get_me()),parse_mode='html')
        elif message.text == "🔙 Отклонить вызов оператора":
            bot.send_message(str(message.chat.id), "❗ Общение с оператором заершено")
            if len(account_settings[str(message.chat.id)]["tags"]) != 0:
                bot.send_message(str(account_settings[str(message.chat.id)]["tags"][0]), "❗ Общение с оператором заершено")
                account_settings[account_settings[str(message.chat.id)]["tags"][0]]['conversation'] = 'close'
                account_settings[account_settings[str(message.chat.id)]["tags"][0]]['tags'].clear()
                with open(path_acc_settings, 'w+') as f:
                    json.dump(account_settings, f, indent='    ')
                with open(path_acc_settings, 'r') as fle:
                    account_settings = json.load(fle)
                if account_settings[account_settings[str(message.chat.id)]["tags"][0]]["language"] == "Русский":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    if account_settings[str(message.chat.id)]["tags"][0] == '281321076' or account_settings[str(message.chat.id)]["tags"][0] == '667068180' or account_settings[str(message.chat.id)]["tags"][0] == '907508218':
                        item1 = types.KeyboardButton("📞 Телефон")
                        item2 = types.KeyboardButton("🏠 Адреса")
                        item4 = types.KeyboardButton("📝 Создать заказ")
                        item5 = types.KeyboardButton("❗️ Оставить жалобу")
                        item10 = types.KeyboardButton("💽 БД переписок")
                        item6 = types.KeyboardButton("% Получить скидку")
                        item7 = types.KeyboardButton("®FAQ Инструкция")
                        item9 = types.KeyboardButton("🌐 Мы в социальных сетях")
                        markup.add(item1, item2, item4, item9, item5, item10, item6, item7)
                    else:
                        item1 = types.KeyboardButton("📞 Телефон")
                        item2 = types.KeyboardButton("🏠 Адреса")
                        item3 = types.KeyboardButton("🙋 Оператор")
                        item4 = types.KeyboardButton("📝 Создать заказ")
                        item5 = types.KeyboardButton("❗️ Оставить жалобу")
                        item6 = types.KeyboardButton("% Получить скидку")
                        item7 = types.KeyboardButton("®FAQ Инструкция")
                        item8 = types.KeyboardButton("✍️ Написать директору")
                        item9 = types.KeyboardButton("🌐 Мы в социальных сетях")
                        markup.row(item1, item2, item4).row(item6, item7, item9).row(item3).row(item8).row(item5)
                    faq_txt = ""
                    with io.open(path_FAQ_label, encoding='utf-8') as file_set:
                        for i in file_set:
                            faq_txt += i
                    bot.send_message(account_settings[str(message.chat.id)]["tags"][0], faq_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    if account_settings[str(message.chat.id)]["tags"][0] == '281321076' or account_settings[str(message.chat.id)]["tags"][0] == '667068180' or account_settings[str(message.chat.id)]["tags"][0] == '907508218':
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
                        item1 = types.KeyboardButton("📞 telefon")
                        item2 = types.KeyboardButton("🏠 manzillari")
                        item3 = types.KeyboardButton("🙋 Operator")
                        item4 = types.KeyboardButton("📝 buyurtma yaratish")
                        item5 = types.KeyboardButton("❗️ Shikoyat qoldiring")
                        item6 = types.KeyboardButton("% Chegirma oling")
                        item7 = types.KeyboardButton("®FAQ Ko'rsatma")
                        item8 = types.KeyboardButton("✍️ Direktorga yozing")
                        item9 = types.KeyboardButton("🌐 Biz ijtimoiy tarmoqlarda")
                        markup.row(item1, item2, item4).row(item6, item7, item9).row(item3).row(item8).row(item5)
                    faq_txt = ""
                    with io.open(path_sec_FAQ_label, encoding='utf-8') as file_set:
                        for i in file_set:
                            faq_txt += i
                    bot.send_message(account_settings[str(message.chat.id)]["tags"][0], faq_txt.format(message.chat, bot.get_me()), parse_mode='html', reply_markup=markup)
            keyboardRefMaker(message)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("👍", callback_data='👍')
            item2 = types.InlineKeyboardButton("👎", callback_data="👎")
            markup.add(item1, item2)
            if message.chat.id == 281321076 or message.chat.id == 667068180 or message.chat.id == 263305395 or message.chat.id == 666803198 or message.chat.id == 907508218:
                if account_settings[account_settings[str(message.chat.id)]["tags"][0]]["language"] == "Русский": 
                    bot.send_message(account_settings[str(message.chat.id)]["tags"][0], 'Оцените работу оператора!', reply_markup=markup)
                else: bot.send_message(account_settings[str(message.chat.id)]["tags"][0], 'Operator ishini baholang!', reply_markup=markup)
            else:
                if account_settings[str(message.chat.id)]["language"] == "Русский": 
                    bot.send_message(str(message.chat.id), 'Оцените работу оператора!', reply_markup=markup)
                else: bot.send_message(str(message.chat.id), 'Operator ishini baholang!', reply_markup=markup)
            account_settings[str(message.chat.id)]['conversation'] = 'close'
            account_settings[str(message.chat.id)]['tags'].clear()
            with open(path_acc_settings, 'w+') as f:
                json.dump(account_settings, f, indent='    ')
            with open(path_acc_settings, 'r') as fle:
                account_settings = json.load(fle)
            closerDataBase(str(message.chat.id))
        elif message.text == "🔙 Operator chaqiruvini rad etish":
            bot.send_message(str(message.chat.id), "❗ Operator bilan aloqa yakunlandi")
            if len(account_settings[str(message.chat.id)]["tags"]) != 0:
                bot.send_message(str(account_settings[str(message.chat.id)]["tags"][0]), "❗ Operator bilan aloqa yakunlandi")
                account_settings[account_settings[str(message.chat.id)]["tags"][0]]['conversation'] = 'close'
                account_settings[account_settings[str(message.chat.id)]["tags"][0]]['tags'].clear()
                if account_settings[account_settings[str(message.chat.id)]["tags"][0]]["language"] == "Русский":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    if account_settings[str(message.chat.id)]["tags"][0] == 281321076 or account_settings[str(message.chat.id)]["tags"][0] == 667068180 or account_settings[str(message.chat.id)]["tags"][0] == 907508218:
                        item1 = types.KeyboardButton("📞 Телефон")
                        item2 = types.KeyboardButton("🏠 Адреса")
                        item4 = types.KeyboardButton("📝 Создать заказ")
                        item5 = types.KeyboardButton("❗️ Оставить жалобу")
                        item10 = types.KeyboardButton("💽 БД переписок")
                        item6 = types.KeyboardButton("% Получить скидку")
                        item7 = types.KeyboardButton("®FAQ Инструкция")
                        item9 = types.KeyboardButton("🌐 Мы в социальных сетях")
                        markup.add(item1, item2, item4, item9, item5, item10, item6, item7)
                    else:
                        item1 = types.KeyboardButton("📞 Телефон")
                        item2 = types.KeyboardButton("🏠 Адреса")
                        item3 = types.KeyboardButton("🙋 Оператор")
                        item4 = types.KeyboardButton("📝 Создать заказ")
                        item5 = types.KeyboardButton("❗️ Оставить жалобу")
                        item6 = types.KeyboardButton("% Получить скидку")
                        item7 = types.KeyboardButton("®FAQ Инструкция")
                        item8 = types.KeyboardButton("✍️ Написать директору")
                        item9 = types.KeyboardButton("🌐 Мы в социальных сетях")
                        markup.row(item1, item2, item4).row(item6, item7, item9).row(item3).row(item8).row(item5)
                    faq_txt = ""
                    with io.open(path_FAQ_label, encoding='utf-8') as file_set:
                        for i in file_set:
                            faq_txt += i
                    bot.send_message(account_settings[str(message.chat.id)]["tags"][0], faq_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    if account_settings[str(message.chat.id)]["tags"][0] == 281321076 or account_settings[str(message.chat.id)]["tags"][0] == 667068180 or account_settings[str(message.chat.id)]["tags"][0] == 907508218 :
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
                        item1 = types.KeyboardButton("📞 telefon")
                        item2 = types.KeyboardButton("🏠 manzillari")
                        item3 = types.KeyboardButton("🙋 Operator")
                        item4 = types.KeyboardButton("📝 buyurtma yaratish")
                        item5 = types.KeyboardButton("❗️ Shikoyat qoldiring")
                        item6 = types.KeyboardButton("% Chegirma oling")
                        item7 = types.KeyboardButton("®FAQ Ko'rsatma")
                        item8 = types.KeyboardButton("✍️ Direktorga yozing")
                        item9 = types.KeyboardButton("🌐 Biz ijtimoiy tarmoqlarda")
                        markup.row(item1, item2, item4).row(item6, item7, item9).row(item3).row(item8).row(item5)
                    faq_txt = ""
                    with io.open(path_sec_FAQ_label, encoding='utf-8') as file_set:
                        for i in file_set:
                            faq_txt += i
                    bot.send_message(account_settings[str(message.chat.id)]["tags"][0], faq_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
            keyboardRefMakerSec(message)
            closerDataBase(str(message.chat.id))
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('👍', callback_data='👍')
            item2 = types.InlineKeyboardButton('👎', callback_data='👎')
            markup.add(item1, item2)
            if message.chat.id == 281321076 or message.chat.id == 667068180 or message.chat.id == 263305395 or message.chat.id == 666803198 or message.chat.id == 907508218:
                if account_settings[account_settings[str(message.chat.id)]["tags"][0]]["language"] == "Русский": 
                    bot.send_message(account_settings[str(message.chat.id)]["tags"][0], 'Оцените работу оператора!', reply_markup=markup)
                else: bot.send_message(account_settings[str(message.chat.id)]["tags"][0], 'Operator ishini baholang!', reply_markup=markup)
            else:
                if account_settings[str(message.chat.id)]["language"] == "Русский": 
                    bot.send_message(str(message.chat.id), 'Оцените работу оператора!', reply_markup=markup)
                else: bot.send_message(str(message.chat.id), 'Operator ishini baholang!', reply_markup=markup)
            account_settings[str(message.chat.id)]['conversation'] = 'close'
            account_settings[str(message.chat.id)]['tags'].clear()
            with open(path_acc_settings, 'w+') as f:
                json.dump(account_settings, f, indent='    ')
            with open(path_acc_settings, 'r') as fle:
                account_settings = json.load(fle)
        elif message.text == "❔ Инструкция":
            FAQ_txt = ""
            with io.open(path_FAQoper_label, encoding='utf-8') as file_set:
                for i in file_set:
                    FAQ_txt += i
            bot.send_message(message.chat.id, FAQ_txt.format(message.chat, bot.get_me()),parse_mode='html')
        elif message.text == "❔ Ko'rsatma":
            FAQ_txt = ""
            with io.open(path_sec_FAQoper_label, encoding='utf-8') as file_set:
                for i in file_set:
                    FAQ_txt += i
            bot.send_message(message.chat.id, FAQ_txt.format(message.chat, bot.get_me()),parse_mode='html')
        else: 
            if account_settings[str(message.chat.id)]['conversation'] == 'open':
                if message.chat.id == 281321076 or message.chat.id == 667068180 or message.chat.id == 263305395 or message.chat.id == 666803198 or message.chat.id == 907508218:
                    sm_id = 'Operator: '
                else: sm_id = 'User: '
                if message.text != None:
                    sm_id = sm_id + message.text + '\n'
                    bot.send_message(account_settings[str(message.chat.id)]["tags"][0], message.text)
                elif message.caption != None:
                    sm_id = sm_id + message.caption + '\n'
                    bot.send_message(account_settings[str(message.chat.id)]["tags"][0], message.caption)
                if message.photo != None:
                    sm_id = sm_id + 'PHOTO\n'
                    fileID = message.photo[-1].file_id
                    file_info = bot.get_file(fileID)
                    downloaded_file = bot.download_file(file_info.file_path)
                    #with open("image.jpg", 'wb') as new_file:
                    #    new_file.write(downloaded_file)
                    bot.send_photo(account_settings[str(message.chat.id)]["tags"][0], downloaded_file)
                insert_text_to_data(sm_id, str(message.chat.id))


def saveNewTextStart(message):
    word = message.text
    with open(path_first_lang, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextStart_Sec(message):
    word = message.text
    with open(path_second_lang, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Chenges saved!")

def saveNewTextFAQ(message):
    word = message.text
    with open(path_FAQ_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextFAQ_Sec(message):
    word = message.text
    with open(path_sec_FAQ_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Chenges saved!")    

def saveNewTextSupport(message):
    word = message.text
    with open(path_oper_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextSupport_Sec(message):
    word = message.text
    with open(path_sec_oper_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Chenges saved!")

def saveNewTextTele(message):
    word = message.text
    with open(path_telephone_num, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextTele_Sec(message):
    word = message.text
    with open(path_sec_telephone_num, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "O'zgarishlar saqlandi!")

def saveNewTextAdress(message):
    word = message.text
    with open(path_address_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextAdress_Sec(message):
    word = message.text
    with open(path_sec_address_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Chenges saved!")

def saveNewTextOrder(message):
    word = message.text
    with open(path_order_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "O'zgarishlar saqlandi!")
def saveNewTextOrder_Sec(message):
    word = message.text
    with open(path_sec_order_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Chenges saved!")

def saveNewTextRecv(message):
    word = message.text
    with open(path_recv_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextRecv_Sec(message):
    word = message.text
    with open(path_sec_recv_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Chenges saved!")

def saveNewTextDisc(message):
    word = message.text
    with open(path_discount_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextDisc_Sec(message):
    word = message.text
    with open(path_sec_discount_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "O'zgarishlar saqlandi!")
  
def saveNewTextSocial(message):
    word = message.text
    with open(path_social_web, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextSocial_Sec(message):
    word = message.text
    with open(path_sec_social_web, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "O'zgarishlar saqlandi!")

def saveNewTextOperFAQ(message):
    word = message.text
    with open(path_FAQoper_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "Изменения сохранены!")
def saveNewTextOperFAQ_Sec(message):
    word = message.text
    with open(path_sec_FAQoper_label, 'w', encoding='utf-8') as f:
        f.write(word)
    bot.send_message(message.chat.id, "O'zgarishlar saqlandi!")


def keyboardRefMaker(message):
    global account_settings
    if message.chat.id == 281321076 or message.chat.id == 667068180 or message.chat.id == 907508218 or message.chat.id == 263305395 or message.chat.id == 666803198:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("📞 Телефон")
        item2 = types.KeyboardButton("🏠 Адреса")
        item4 = types.KeyboardButton("📝 Создать заказ")
        item5 = types.KeyboardButton("❗️ Оставить жалобу")
        item10 = types.KeyboardButton("💽 БД переписок")
        item6 = types.KeyboardButton("% Получить скидку")
        item7 = types.KeyboardButton("®FAQ Инструкция")
        item9 = types.KeyboardButton("🌐 Мы в социальных сетях")
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
        item9 = types.KeyboardButton("🌐 Мы в социальных сетях")
        markup.row(item1, item2, item4).row(item6, item7, item9).row(item3).row(item8).row(item5)
    faq_txt = ""
    with io.open(path_FAQ_label, encoding='utf-8') as file_set:
        for i in file_set:
            faq_txt += i
    bot.send_message(message.chat.id, faq_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
    with open(path_acc_settings, 'r') as fle:
        account_settings = json.load(fle)
    account_settings[str(message.chat.id)]["personal data"] = "YES"
    with open(path_acc_settings, 'w+') as f:
        json.dump(account_settings, f, indent='    ')
    with open(path_acc_settings, 'r') as fle:
        account_settings = json.load(fle)
def keyboardRefMakerSec(message):
    if message.chat.id == 281321076 or message.chat.id == 667068180 or message.chat.id == 907508218 or message.chat.id == 263305395 or message.chat.id == 666803198:
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
        markup.row(item1, item2, item4).row(item6, item7, item9).row(item3).row(item8).row(item5)
    faq_txt = ""
    with io.open(path_sec_FAQ_label, encoding='utf-8') as file_set:
        for i in file_set:
            faq_txt += i
    bot.send_message(message.chat.id, faq_txt.format(message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
    with open(path_acc_settings, 'r') as fle:
        account_settings = json.load(fle)
    account_settings[str(message.chat.id)]["personal data"] = "YES"
    with open(path_acc_settings, 'w+') as f:
        json.dump(account_settings, f, indent='    ')
    with open(path_acc_settings, 'r') as fle:
        account_settings = json.load(fle)


def fdbackName(message):
    global feed_back
    global account_settings
    name_user = message.text
    if name_user != 'stop':
        if name_user == None: name_user = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)] = {"Name" : name_user, "Username" : str(message.chat.username), "Language" : account_settings[str(message.chat.id)]["language"]}
        send = bot.send_message(message.chat.id, '➕ Введите ваш номер телефона')
        bot.register_next_step_handler(send, fdbackTele)
    else:
        bot.send_message(message.chat.id, '➕ Операция отменена')
def fdbackTele(message):
    global feed_back
    tele_num = message.text
    if tele_num.isdigit() == True:
        if tele_num == None: tele_num = 'Пользователь отправил нечитаемый объект'
        bot.send_message(message.chat.id, '➕ Жалоба составляется в четыре этапа:\n1) Причина жалобы\n2) Обозначение филиала/места, где произошёл инцидент\n3) Дату инцидента\n4) Имя или опишите оппонента, с которым произошёл конфликт\n❌ Для отмены операции напишите stop')
        feed_back[str(message.chat.id)].update({"Telephone number" : tele_num})
        send = bot.send_message(message.chat.id, '➕ Напишите причину жалобы')
        bot.register_next_step_handler(send, fdbackReason)
    elif tele_num == 'stop':
        bot.send_message(message.chat.id, '➕ Операция отменена')
    else:
        send = bot.send_message(message.chat.id, '➕ Введите номер телефона в формате 87777777777 или напишите stop')
        bot.register_next_step_handler(send, fdbackTele)
def fdbackReason(message):
    global feed_back
    reason_send = message.text
    if reason_send != 'stop':
        if reason_send == None: reason_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Reason" : reason_send})
        send = bot.send_message(message.chat.id, '➕ Напишите филиал/место, где произошёл инцидент')
        bot.register_next_step_handler(send, fdbackPlace)
    else:
        bot.send_message(message.chat.id, '➕ Операция отменена')
def fdbackPlace(message):
    global feed_back
    place_send = message.text
    if place_send != 'stop':
        if place_send == None: place_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Place" : place_send})
        send = bot.send_message(message.chat.id, '➕ Напишите дату инцидента')
        bot.register_next_step_handler(send, fdbackDate)
    else:
        bot.send_message(message.chat.id, '➕ Операция отменена')
def fdbackDate(message):
    global feed_back
    date_send = message.text
    if date_send != 'stop':
        if date_send == None: date_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Date" : date_send})
        send = bot.send_message(message.chat.id, '➕ Напишите имя или опишите оппонента, с которым произошёл конфликт')
        bot.register_next_step_handler(send, fdBack_fill)
    else:
        bot.send_message(message.chat.id, '➕ Операция отменена')
def fdBack_fill(message):
    global feed_back
    global txt
    feedback_user = message.text
    if feedback_user != '📞 Телефон' and feedback_user != '💽 БД переписок' and feedback_user !='🏠 Адреса' and feedback_user !='🌐 Мы в социальных сетях' and feedback_user !='🙋 Оператор' and feedback_user != '✍️ Написать директору' and feedback_user !='📝 Создать заказ' and feedback_user !='❗️ Оставить жалобу' and feedback_user !='% Получить скидку' and feedback_user !='®FAQ Инструкция' and feedback_user != 'stop':
        if feedback_user == None: feedback_user = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})
        txt = "--------ЖАЛОБА--------\n"
        txt += "id: "
        txt += str(message.chat.id)
        txt += "\nИмя: "
        txt += feed_back[str(message.chat.id)]["Name"]
        txt += "\nНомер телефона: "
        txt += feed_back[str(message.chat.id)]["Telephone number"]
        txt += "\nЯзык: "
        txt += account_settings[str(message.chat.id)]["language"]
        txt += "\nПричина: "
        txt += feed_back[str(message.chat.id)]["Reason"]
        txt += "\nМесто: "
        txt += feed_back[str(message.chat.id)]["Place"]
        txt += "\nДата: "
        txt += feed_back[str(message.chat.id)]["Date"]
        txt += "\nКонфликт: "
        txt += feedback_user
        txt += "\n---------------------"
        bot.send_message(message.chat.id, '➕ Контроль сервиса лаборатории SwissLab. Мы благодарим за сделанный выбор и будем рады, если вы поможете улучшить качество нашего сервиса!\n🙋 Наш оператор свяжется с вами при необходимости!')
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Ответить", callback_data='Q' + str(message.chat.id))
        markup.add(item1)
        try:
            bot.send_message(281321076, txt, reply_markup=markup)
        except Exception as e:
            print('User 281321076 blocked!')
        try:
            bot.send_message(667068180, txt, reply_markup=markup)
        except Exception as e:
            print('User 667068180 blocked!')
        try:
            bot.send_message(263305395, txt, reply_markup=markup)
        except Exception as e:
            print('User 263305395 blocked!')
        try:
            bot.send_message(666803198, txt, reply_markup=markup)
        except Exception as e:
            print('User 666803198 blocked!')
        try:
            bot.send_message(907508218, txt, reply_markup=markup)
        except Exception as e:
            print('User 907508218 blocked!')
        oper_id = '0'
        insert_new_feedback_data(oper_id,  str(message.chat.id), txt)
    elif feedback_user == 'stop':
        bot.send_message(message.chat.id, '➕ Операция отменена')
    else:
        send = bot.send_message(message.chat.id, '➕ Введите ваш отзыв в правильном формате или напишите stop')
        bot.register_next_step_handler(send, fdBack_fill)

def fdbackName_Sec(message):
    global feed_back
    global account_settings
    name_user = message.text
    if name_user != 'stop':
        if name_user == None: name_user = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)] = {"Name" : name_user, "Username" : str(message.chat.username), "Language" : account_settings[str(message.chat.id)]["language"]}
        send = bot.send_message(message.chat.id, '➕ Telefon raqamingizni kiriting')
        bot.register_next_step_handler(send, fdbackTele_Sec)
    else:
        bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
def fdbackTele_Sec(message):
    global feed_back
    tele_num = message.text
    if tele_num.isdigit() == True:
        if tele_num == None: tele_num = 'Пользователь отправил нечитаемый объект'
        bot.send_message(message.chat.id, '➕ Shikoyat tort bosqichda tuziladi:\n1) Shikoyat sababi\n2) Hodisa sodir bolgan filial/joyni belgilash\n3) Hodisa sanasi\n4) Mojaro yuz bergan raqibning nomi yoki tarifi\n❌ Operatsiyani bekor qilish uchun yozing stop')
        feed_back[str(message.chat.id)].update({"Telephone number" : tele_num})
        send = bot.send_message(message.chat.id, '➕ Shikoyat sababini yozing')
        bot.register_next_step_handler(send, fdbackReason_Sec)
    elif tele_num == 'stop':
        bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
    else:
        send = bot.send_message(message.chat.id, '➕ Telefon raqamingizni formatda kiriting 9997777777777 yoki yozing stop')
        bot.register_next_step_handler(send, fdbackTele_Sec)
def fdbackReason_Sec(message):
    global feed_back
    reason_send = message.text
    if reason_send != 'stop':
        if reason_send == None: reason_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Reason" : reason_send})
        send = bot.send_message(message.chat.id, '➕ Hodisa sodir bolgan filial/joyni yozing')
        bot.register_next_step_handler(send, fdbackPlace_Sec)
    else:
        bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
def fdbackPlace_Sec(message):
    global feed_back
    place_send = message.text
    if place_send != 'stop':
        if place_send == None: place_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Place" : place_send})
        send = bot.send_message(message.chat.id, '➕ Hodisa tarixini yozing')
        bot.register_next_step_handler(send, fdbackDate_Sec)
    else:
        bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
def fdbackDate_Sec(message):
    global feed_back
    date_send = message.text
    if date_send != 'stop':
        if date_send == None: date_send = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"Date" : date_send})
        send = bot.send_message(message.chat.id, '➕ Ismni yozing yoki ziddiyatga duch kelgan raqibni tariflang')
        bot.register_next_step_handler(send, fdBack_fill_Sec)
    else:
        bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
def fdBack_fill_Sec(message):
    global feed_back
    global txt
    feedback_user = message.text
    if feedback_user != '📞 telefon' and feedback_user != '💽 Yozishmalar bazasi' and feedback_user !='🏠 manzillari' and feedback_user !='🌐 Biz ijtimoiy tarmoqlarda' and feedback_user !='🙋 Operator' and feedback_user != '✍️ Direktorga yozing' and feedback_user !='📝 buyurtma yaratish' and feedback_user !='❗️ Shikoyat qoldiring' and feedback_user !='% Chegirma oling' and feedback_user !="®FAQ Ko'rsatma" and feedback_user != 'stop':
        if feedback_user == None: feedback_user = 'Пользователь отправил нечитаемый объект'
        feed_back[str(message.chat.id)].update({"FeedBack" : feedback_user})
        txt = "--------ЖАЛОБА--------\n"
        txt += "id: "
        txt += str(message.chat.id)
        txt += "\nИмя: "
        txt += feed_back[str(message.chat.id)]["Name"]
        txt += "\nНомер телефона: "
        txt += feed_back[str(message.chat.id)]["Telephone number"]
        txt += "\nЯзык: "
        txt += account_settings[str(message.chat.id)]["language"]
        txt += "\nПричина: "
        txt += feed_back[str(message.chat.id)]["Reason"]
        txt += "\nМесто: "
        txt += feed_back[str(message.chat.id)]["Place"]
        txt += "\nДата: "
        txt += feed_back[str(message.chat.id)]["Date"]
        txt += "\nКонфликт: "
        txt += feedback_user
        txt += "\n---------------------"
        bot.send_message(message.chat.id, '➕ Laboratoriya xizmatini nazorat qilish SwissLab. Biz tanlaganingiz uchun tashakkur va xizmatimiz sifatini yaxshilashga yordam bersangiz xursand bolamiz!\n🙋 Agar kerak bolsa, bizning operatorimiz sizga murojaat qiladi!')
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Ответить", callback_data='Q' + str(message.chat.id))
        markup.add(item1)
        try:
            bot.send_message(281321076, txt, reply_markup=markup)
        except Exception as e:
            print('User 281321076 blocked!')
        try:
            bot.send_message(667068180, txt, reply_markup=markup)
        except Exception as e:
            print('User 667068180 blocked!')
        try:
            bot.send_message(263305395, txt, reply_markup=markup)
        except Exception as e:
            print('User 263305395 blocked!')
        try:
            bot.send_message(666803198, txt, reply_markup=markup)
        except Exception as e:
            print('User 666803198 blocked!')
        try:
            bot.send_message(907508218, txt, reply_markup=markup)
        except Exception as e:
            print('User 907508218 blocked!')
        oper_id = '0'
        insert_new_feedback_data(oper_id,  str(message.chat.id), txt)
    elif feedback_user == 'stop':
        bot.send_message(message.chat.id, '➕ Amal bekor qilindi')
    else:
        send = bot.send_message(message.chat.id, '➕ Iltimos, sharhingizni togri formatda kiriting yoki yozing stop')
        bot.register_next_step_handler(send, fdBack_fill_Sec)


def enterTag(message):
    global account_settings
    global mess
    tags = message.text
    if mess == "new":
        account_settings[str(message.chat.id)]["tags"] = []
        mess = ""
        with open(path_acc_settings, 'w+') as f:
            json.dump(account_settings, f, indent='    ')
        with open(path_acc_settings, 'r') as fle:
            account_settings = json.load(fle)
    account_settings[str(message.chat.id)]["tags"].append(tags)
    with open(path_acc_settings, 'w+') as f:
        json.dump(account_settings, f, indent='    ')
    with open(path_acc_settings, 'r') as fle:
        account_settings = json.load(fle)
    it = len(account_settings[str(message.chat.id)]["tags"])
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
        account_settings[str(message.chat.id)]["tags"] = []
        mess = ""
        with open(path_acc_settings, 'w+') as f:
            json.dump(account_settings, f, indent='    ')
        with open(path_acc_settings, 'r') as fle:
            account_settings = json.load(fle)
    account_settings[str(message.chat.id)]["tags"].append(tags)
    with open(path_acc_settings, 'w+') as f:
        json.dump(account_settings, f, indent='    ')
    with open(path_acc_settings, 'r') as fle:
        account_settings = json.load(fle)
    it = len(account_settings[str(message.chat.id)]["tags"])
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
    if account_settings[str(message.chat.id)]["language"] == "Русский":
        bot.send_photo(message.chat.id, contents, caption='💳 Ваша карта')
    else:
        bot.send_photo(message.chat.id, contents, caption='💳 Sizning kartangiz')
    os.remove('newAcc.png')


def refAdd(message):
    global account_settings
    ref_n = message.text
    with open(path_acc_settings, 'r') as fle:
        account_settings = json.load(fle)
    ch_ref = "none"
    for k in account_settings.keys():
        if k == ref_n:
            ch_ref = "yes"
            break
    if ch_ref == "yes":
        if int(account_settings[ref_n]["ref"]) < 10:
            account_settings[ref_n]["ref"] = str(int(account_settings[ref_n]["ref"]) + 1)
            with open(path_acc_settings, 'w+') as f:
                json.dump(account_settings, f, indent='    ')
            with open(path_acc_settings, 'r') as fle:
                account_settings = json.load(fle)
            if account_settings[str(message.chat.id)]["language"] == "Русский":
                bot.send_message(message.chat.id, "✅ Спасибо за активацию!")
                bot.send_message(ref_n, "✅ Новый пользователь активировал реферальный код!")
                keyboardRefMaker(message)
            else:
                bot.send_message(message.chat.id, "✅ Faollashtirish uchun rahmat!")
                bot.send_message(ref_n, "✅ Yangi foydalanuvchi tavsiya kodini faollashtirdi!")
                keyboardRefMakerSec(message)
        else:
            if account_settings[str(message.chat.id)]["language"] == "Русский":
                bot.send_message(message.chat.id, "⚠️ Активации кода закончены")
                keyboardRefMaker(message)
            else:
                bot.send_message(message.chat.id, "⚠️ Kodni faollashtirish tugadi")
                keyboardRefMakerSec(message)
    elif ref_n == "stop":
        if account_settings[str(message.chat.id)]["language"] == "Русский":
            keyboardRefMaker(message)
        else:
            keyboardRefMakerSec(message)
    else:
        if account_settings[str(message.chat.id)]["language"] == "Русский":
            send = bot.send_message(message.chat.id, '❔ Ваш код не найден, поробуйте ещё раз или напишите - stop')
        else: 
            send = bot.send_message(message.chat.id, '❔ Sizning kodingiz topilmadi, yana porobuyte yoki yozing - stop')
        bot.register_next_step_handler(send, refAdd)      


def userSebdText(message):
    global account_settings
    if message.text != 'stop':
        if account_settings[account_settings[str(message.chat.id)]["feedback_st"]]['language'] == 'Русский':
                bot.send_message(account_settings[str(message.chat.id)]["feedback_st"], "Ответ оператора на вашу жалобу!👇")
        else:  bot.send_message(account_settings[str(message.chat.id)]["feedback_st"], "Sizning shikoyatingizga javob beruvchi operator!👇")
        if message.photo != None:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            word_user_send = bot.download_file(file_info.file_path)
            bot.send_photo(account_settings[str(message.chat.id)]["feedback_st"], word_user_send)
        if message.text != None or message.caption != None:
            if message.text != None: word_user_send = message.text
            else: word_user_send = message.caption
            bot.send_message(account_settings[str(message.chat.id)]["feedback_st"], word_user_send)
            insert_new_feedback_data(str(message.chat.id), account_settings[str(message.chat.id)]["feedback_st"] , word_user_send)
        bot.send_message(message.chat.id, "Сообщение отправлено!")
        account_settings[account_settings[str(message.chat.id)]["feedback_st"]]["feedback_st"] = 'close'
        account_settings[str(message.chat.id)]["feedback_st"] = 'close'
        with open(path_acc_settings, 'w+') as f:
            json.dump(account_settings, f, indent='    ')
        with open(path_acc_settings, 'r') as fle:
            account_settings = json.load(fle)
    else: bot.send_message(message.chat.id, 'Операция отменена!')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global new_acc_id
    global account_settings
    global mess
    try:
        if call.data == 'Русский':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            account_settings[new_acc_id]["language"] = "Русский"
            new_acc_id = ""
            with open(path_acc_settings, 'w+') as f:
                json.dump(account_settings, f, indent='    ')
            with open(path_acc_settings, 'r') as fle:
                account_settings = json.load(fle)
            with io.open(path_first_lang, encoding='utf-8') as start_text_file:
                start_txt = ""
                for i in start_text_file:
                    start_txt += i
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Согласен", callback_data='Согласен')
            item2 = types.InlineKeyboardButton("Отказываюсь", callback_data='Отказываюсь')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, start_txt.format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'Отказываюсь':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Вы отказались от обработки персональных данных\n♻️ Для перезапуска бота нажмите /start")
        elif call.data == 'Согласен':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Да", callback_data='Да')
            item2 = types.InlineKeyboardButton("Нет", callback_data='Нет')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "♻️ У вас есть реферальная ссылка?", reply_markup=markup)
        
        elif call.data == 'Нет':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            keyboardRefMaker(call.message)
        elif call.data == 'Да':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Отправьте код')
            bot.register_next_step_handler(send, refAdd)
        
        elif call.data == 'Ozbek':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            account_settings[new_acc_id]["language"] = "Ozbek"
            new_acc_id = ""
            with open(path_acc_settings, 'w+') as f:
                json.dump(account_settings, f, indent='    ')
            with open(path_acc_settings, 'r') as fle:
                account_settings = json.load(fle)
            with io.open(path_second_lang, encoding='utf-8') as start_text_file:
                start_txt = ""
                for i in start_text_file:
                    start_txt += i
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("ROZIMAN", callback_data='Agree')
            item2 = types.InlineKeyboardButton("Qo'shilmayman", callback_data='Disagree')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, start_txt.format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'Disagree':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Siz shaxsiy ma'lumotlarni qayta ishlash uchun rad qilgan\n♻️ Botni qayta ishga tushirish uchun bosing /start")
        elif call.data == 'Agree':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Ha", callback_data='Yes')
            item2 = types.InlineKeyboardButton("Yo'q", callback_data='No')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "♻️ Yo'naltiruvchi havola bormi?", reply_markup=markup)   
        
        elif call.data == 'No':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            keyboardRefMakerSec(call.message)
        elif call.data == 'Yes':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Kodni yuboring')
            bot.register_next_step_handler(send, refAdd)

        elif call.data == 'Написать жалобу':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Напишите ваше имя')
            bot.register_next_step_handler(send, fdbackName)
        elif call.data == 'Write a feedback':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Telefon raqamingizni kiriting')
            bot.register_next_step_handler(send, fdbackName_Sec)

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
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangStart')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangStart')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangStart':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextStart) 
        elif call.data == 'OzbekLangStart':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextStart_Sec) 

        elif call.data == 'FAQ текст':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangFAQ')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangFAQ')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextFAQ) 
        elif call.data == 'OzbekLangFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextFAQ_Sec)

        elif call.data == 'Текст оператора':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangOper')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangOper')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangOper':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextSupport) 
        elif call.data == 'OzbekLangOper':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextSupport_Sec)

        elif call.data == 'Текст телефона':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangTele')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangTele')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangTele':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextTele) 
        elif call.data == 'OzbekLangTele':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextTele_Sec)

        elif call.data == 'Текст адресса':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangAdress')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangAdress')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangAdress':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextAdress) 
        elif call.data == 'OzbekLangAdress':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextAdress_Sec)

        elif call.data == 'Текст создания заказа':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangOrder')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangOrder')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangOrder':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextOrder) 
        elif call.data == 'OzbekLangOrder':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextOrder_Sec)       

        elif call.data == 'Текст отзыва':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangRecv')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangRecv')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangRecv':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextRecv) 
        elif call.data == 'OzbekLangRecv':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextRecv_Sec)            
        
        elif call.data == 'Текст скидки':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangDisc')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangDisc')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangDisc':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextDisc) 
        elif call.data == 'OzbekLangDisc':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextDisc_Sec)            

        elif call.data == 'Текст социальные сети':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangSocial')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangSocial')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)
        elif call.data == 'РусскийLangSocial':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextSocial) 
        elif call.data == 'OzbekLangSocial':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextSocial_Sec)       
        
        elif call.data == 'Текст инструкции оператора':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Русский", callback_data='РусскийLangOperFAQ')
            item2 = types.InlineKeyboardButton("Ozbek", callback_data='OzbekLangOperFAQ')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, "Выберите язык блока".format(call.message.chat, bot.get_me()),parse_mode='html', reply_markup=markup)   
        elif call.data == 'РусскийLangOperFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, '➕ Введите текст для изменения')
            bot.register_next_step_handler(send, saveNewTextOperFAQ) 
        elif call.data == 'OzbekLangOperFAQ':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send = bot.send_message(call.message.chat.id, "➕ Введите текст для изменения")
            bot.register_next_step_handler(send, saveNewTextOperFAQ_Sec)  

        elif call.data == '👍':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if account_settings[str(call.message.chat.id)]["language"] == "Русский":
                bot.send_message(call.message.chat.id, 'Спасибо за оценку!')
            else: bot.send_message(call.message.chat.id, 'Baholash uchun rahmat!')
        elif call.data == '👎':
            bot.delete_message(call.message.chat.id, call.message.message_id) 
            if account_settings[str(call.message.chat.id)]["language"] == "Русский":
                bot.send_message(call.message.chat.id, 'Спасибо за оценку!')
            else: bot.send_message(call.message.chat.id, 'Baholash uchun rahmat!')
            
        elif call.data[0] == 'Q':
            if account_settings[call.data[1:]]["feedback_st"] == 'open':
                account_settings[call.data[1:]]["feedback_st"] = 'close'
                account_settings[str(call.message.chat.id)]["feedback_st"] = call.data[1:]
                with open(path_acc_settings, 'w+') as f:
                    json.dump(account_settings, f, indent='    ')
                with open(path_acc_settings, 'r') as fle:
                    account_settings = json.load(fle)
                send = bot.send_message(call.message.chat.id, "➕ Введите текст для ответа пользователю")
                bot.register_next_step_handler(send, userSebdText)
            else:
                bot.send_message(call.message.chat.id, "Оператор уже ответил этому пользователю!\nДля отмены повторного ответа напишите stop")
                account_settings[call.data[1:]]["feedback_st"] = 'close'
                account_settings[str(call.message.chat.id)]["feedback_st"] = call.data[1:]
                with open(path_acc_settings, 'w+') as f:
                    json.dump(account_settings, f, indent='    ')
                with open(path_acc_settings, 'r') as fle:
                    account_settings = json.load(fle)
                send = bot.send_message(call.message.chat.id, "➕ Введите текст для ответа пользователю")
                bot.register_next_step_handler(send, userSebdText)
        else:
            if account_settings[str(call.message.chat.id)]["conversation"] == 'close':
                for k in account_settings.keys():
                    if k == call.data and account_settings[k]["conversation"] == 'mid':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton("🔙 Отклонить вызов оператора")
                        item2 = types.KeyboardButton("❔ Инструкция")
                        markup.add(item1, item2)
                        account_settings[str(call.message.chat.id)]["tags"].append(str(k))
                        account_settings[str(call.message.chat.id)]["conversation"] = 'open'
                        account_settings[k]["tags"].append(str(call.message.chat.id))
                        account_settings[k]["tags"].append("0")
                        account_settings[k]["conversation"] = 'open'
                        with open(path_acc_settings, 'w+') as f:
                            json.dump(account_settings, f, indent='    ')
                        with open(path_acc_settings, 'r') as fle:
                            account_settings = json.load(fle)
                        if account_settings[k]["language"] == "Русский":
                            bot.send_message(k, "📞 Найден оператор, переписка активирована")
                        else: 
                            bot.send_message(k, "📞 Operator topildi, yozishmalar faollashtirildi")
                        bot.send_message(str(call.message.chat.id), "📞 Вы подтвердили заявку!", reply_markup=markup)
                        user_id = str(k) 
                        oper_id = str(call.message.chat.id)
                        insert_new_data(user_id, oper_id)
                        break
                if account_settings[str(call.message.chat.id)]["conversation"] != 'open':
                    u_tex = "Пользователь id: "
                    u_tex += str(call.data)
                    u_tex += " отменил режим!\nПовторный вызов..."
                    bot.send_message(call.message.chat.id, u_tex)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("🔙 Отклонить вызов оператора")
                    item2 = types.KeyboardButton("❔ Инструкция")
                    markup.add(item1, item2)
                    account_settings[str(call.message.chat.id)]["tags"].append(str(call.data))
                    account_settings[str(call.message.chat.id)]["conversation"] = 'open'
                    account_settings[str(call.data)]["tags"].append(str(call.message.chat.id))
                    account_settings[str(call.data)]["tags"].append("0")
                    account_settings[str(call.data)]["conversation"] = 'open'
                    with open(path_acc_settings, 'w+') as f:
                        json.dump(account_settings, f, indent='    ')
                    with open(path_acc_settings, 'r') as fle:
                        account_settings = json.load(fle)
                    try:
                        if account_settings[str(call.data)]["language"] == "Русский":
                            bot.send_message(str(call.data), "📞 Оператор активировал переписку", reply_markup=markup)
                        else: 
                            bot.send_message(str(call.data), "📞 Operator yozishmalarni faollashtirdi", reply_markup=markup)
                        bot.send_message(str(call.message.chat.id), "📞 Вы подтвердили заявку!", reply_markup=markup)
                        user_id = str(call.data) 
                        oper_id = str(call.message.chat.id)
                        insert_new_data(user_id, oper_id)
                    except Exception as e:
                        account_settings[str(call.message.chat.id)]["conversation"] = 'close'
                        account_settings[str(call.data)]["tags"] = []
                        account_settings[str(call.message.chat.id)]["tags"] = []
                        bot.send_message(call.message.chat.id, 'Пользователь выключил бота!')
                        with open(path_acc_settings, 'w+') as f:
                            json.dump(account_settings, f, indent='    ')
                        with open(path_acc_settings, 'r') as fle:
                            account_settings = json.load(fle)
                    
            else:
                bot.send_message(call.message.chat.id, "Закончите старый диалог, чтобы начать новый!")

        #show alert
        #bot.answer_callback_query(callback_query_id=call.id, show_alert=False,text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))
        
#RUN
if __name__ == '__main__':
    start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass
