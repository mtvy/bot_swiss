### defs for database conv
from lib import classes, psycopg2, datetime, account_settings

def connect():
    try:
        con = psycopg2.connect(database="postgres",user="postgres",password="postgres", host="127.0.0.1",port="5432")
        cur = con.cursor()
        return con, cur
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting PostgreSQL!", error)
        return 0

def insert_new_data(user_id, oper_id, bot):
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
def insert_new_feedback_data(oper_id, user_id, txt, bot):
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
                txt_db_com = "UPDATE feedback_tb SET status = 'close' WHERE status = 'open' AND user_id = " + user_id
                cur.execute(txt_db_com)
                con.commit()
                return 1
        except Exception as e:
            print('Error entering new data to feedback_tb!', e)
            return 0

def insert_text_to_data(text_val, sm_id, bot):
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

def closerDataBase(sm_id, bot):
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

def getDataFromDB(date_start, bot):
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
def getDataFromFeedBackDB(date_start, bot):
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

def getTextFromDB(id_text, bot):
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
def getTextFromFeedBackDB(id_text, bot):
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

def change_data(name, bot):
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

### For collection

def dbCollection():
    pass

### For account_tb

def insert_account_data(account):
    con, cur = connect()
    if con == 0 and cur == 0:
        return False
    else:
        try:
            cur.execute("INSERT INTO account_tb (telegram_id, login, name, oper_ids, conversation, discount, tags, ref, personal_data, language, feedback_st, timer_conv) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (account.telegram_id, account.login, account.name, account.oper_ids, account.conversation, account.discount, account.tags, account.ref, account.personal_data, account.language, account.feedback_st, account.timer_conv))
            con.commit()
            print('New user add!')
            return True
        except Exception as error:
            print('Error entering new data to account_tb!', error)
            return False

def change_account_data(account, parametr, data):
    con, cur = connect()
    if con == 0 and cur == 0:
        return False
    else:
        try:
            cur.execute("UPDATE account_tb SET " + parametr + " = %s WHERE telegram_id = %s", ( data, account.telegram_id))
            con.commit()
            #print('Successful account_tb update!')
            return True
        except Exception as error:
            print('Error changing data in account_tb!', error)
            return False

def get_accounts_data():
    con, cur = connect()
    if con == 0 and cur == 0:
        return {}
    else:
        try:
            account_settings = {}
            cur.execute("SELECT telegram_id, login, name, oper_ids, conversation, discount, tags, ref, personal_data, language, feedback_st, timer_conv FROM account_tb")
            accounts = cur.fetchall()
            for acc in accounts:
                account = classes.Account(acc = acc)
                account_settings[account.telegram_id] = account
            con.commit()
            #print('Successful account_tb data taken!')
            return account_settings
        except Exception as e:
            print('Error taking data from account_tb!', e)
            return {}
