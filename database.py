import classes, variables, psycopg2, datetime, path, debug, traceback

def connect():
    try:
        con = psycopg2.connect(database = 'postgres' ,
                               password = 'postgres' ,
                               user     = 'postgres' ,
                               host     = '127.0.0.1',
                               port     = '5432'     )        
        
        return con, con.cursor()
    
    except (Exception, psycopg2.DatabaseError) as error:
        debug.saveLogs(f'ERROR! Wrong database connection.\n\n{traceback.format_exc()}', path.log_file)
    
    return (False, False)

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
                return True
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
                return text_adder
        except Exception as e:
            print('Error entering new data to message_tb!', e)
            return False

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


### For message_tb and feedback_tb

def getDataFromDB(date_start, action, row_dict = {'message_tb' : 'date_start', 'feedback_tb' : 'date_enter'}):
    con, cur = connect()
    account_settings = get_accounts_data()
    if con == 0 and cur == 0: return 0
    else:
        try:
            cur.execute(f"SELECT id, user_id FROM {action} WHERE {row_dict[action]} = '{date_start}'")
            text_adder = 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n'
            for i in cur.fetchall():
                for k in account_settings:
                    if k == str(i[1]):
                        name_id = f"@{account_settings[k].login}" if account_settings[k].login != 'None' else account_settings[k].name
                        break
                text_adder = f"{text_adder}{str(i[0])}) Name: {name_id} --- Id: {str(i[1])}\n"
            con.commit()
            return text_adder if text_adder != 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n' else 0
        except Exception as e:
            print(f"Error data {action}!", e)
            return 0

def getTextFromDB(id_text, action, row_dict = {'message_tb' : 'text', 'feedback_tb' : 'text_fb'}):
    con, cur = connect()
    if con == 0 and cur == 0: return 0
    else:
        try:
            cur.execute(f"SELECT {row_dict[action]} FROM {action} WHERE id = {id_text}")
            con.commit()
            return cur.fetchall()[0][0]
        except Exception as e:
            print('Error, wrong id!', e)
            return 0


### For collection

def checkPulldbData(cur, action = None, step = None):
    return cur.fetchall() if action == 'show_data' or step == 9 else True

def dbCollection(message, person_id, step = None, database_push_data = None, action = None, status = None, bot = None):
    """
    To create table: create table collection_tb(id serial primary key, admin_id varchar(128), cashier_id varchar(128), office varchar(128), terminal_number text, cash text, cash_return_info text, doc_number text, PCR text, PCR_express text, analyzes_count text, comment text, admin_date varchar(128), cashier_date varchar(128), status varchar(128));
     ____________________________________________________________________________________________________________________________________________________
    |id|admin_id|cashier_id|office|terminal_number|cash|cash_return_info|doc_number|PCR|PCR_express|analyzes_count|comment|admin_date|cashier_date|status|
    |__|________|__________|______|_______________|____|________________|__________|___|___________|______________|_______|__________|____________|______|
    """
    con, cur = connect()
    if con == 0 and cur == 0: return False
    else:
        try:
            if step == 0:
                database_text_commmit = f"INSERT INTO collection_tb (admin_id, office, admin_date, status) VALUES ('{person_id}', '{message.text}', '{str(datetime.date.today())}', 'admin')"
            elif action == 'cashier_init':
                database_text_commmit = f"UPDATE collection_tb set cashier_id = '{person_id}' WHERE office = '{database_push_data}' AND status = 'cashier'"
            elif step in [1,2,3,4,5,6,7,8] and action == 'show_data':
                database_text_commmit = f"UPDATE collection_tb set {variables.select_collection_action_dict[step]} = '{database_push_data if database_push_data != None else message.text}' WHERE (admin_id = '{person_id}' AND status = 'admin') OR (cashier_id = '{person_id}' AND status = 'cashier')"
                cur.execute(database_text_commmit)
                database_text_commmit = f"SELECT * FROM collection_tb WHERE (admin_id = '{person_id}' AND status = 'admin') OR (cashier_id = '{person_id}' AND status = 'cashier')"
            elif step in [1,2,3,4,5,6,7,8]:
                database_text_commmit = f"UPDATE collection_tb set {variables.select_collection_action_dict[step]} = '{database_push_data if database_push_data != None else message.text}' WHERE admin_id = '{person_id}' AND status = 'admin'"
            elif action == 'send_collection_to_oper':
                database_text_commmit = f"UPDATE collection_tb set status = 'cashier' WHERE status = 'admin' AND admin_id = '{person_id}'"
            elif action == 'confirm_collection':
                database_text_commmit = f"UPDATE collection_tb set status = 'confirmed' WHERE status = 'cashier' AND cashier_id = '{person_id}'"
            elif action == 'show_collection_to_cashier':
                database_text_commmit = f"SELECT * FROM collection_tb WHERE status = 'cashier' AND office = '{database_push_data}'"
            elif step == 9:
                database_text_commmit = f"SELECT * FROM collection_tb WHERE status = '{database_push_data}' AND (admin_id = '{person_id}' OR cashier_id = '{person_id}')"
            cur.execute(database_text_commmit)
            data = checkPulldbData(cur = cur, action = action, step = step)
            con.commit()
            print('New collection add by admin!')
            return data
        except Exception as error:
            print('Error entering new data to collection_tb!', error)
            return False


### For check MESSAGE_ID
def dbMessageId(action, message_id = None):
    """
    This definition hanles id of posting message.
    To create table: create table messageId_tb(message_id integer);
    """
    con, cur = connect()
    if con == 0 and cur == 0: return False
    else:
        try:
            if action == 'take_id': database_text_commmit = 'SELECT message_id FROM messageId_tb'
            elif action == 'save_id': database_text_commmit = f"UPDATE messageId_tb set message_id = {message_id}"
            elif action == 'init_id': database_text_commmit = f"INSERT INTO messageId_tb (message_id) VALUES ({message_id})"
            cur.execute(database_text_commmit)
            data = checkPulldbData(cur = cur, action = 'show_data' if action == 'take_id' else None)
            con.commit()
            return data
        except Exception as error:
            print('Error changing data in messageId_tb!', error)
            return False


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

def test_database() -> bool:
    
    test_connect, _ = connect()
    debug.saveLogs(f'CONNECTION [{True if test_connect else False}] <- connect()\n\n', path.log_file)

    test_insert_data = insert_new_data('0', '0')
    debug.saveLogs(f'CONNECTION [{True if test_connect else False}] <- connect()\n\n', path.log_file)

    

if __name__ == "__main__":
    test_database()


    