import classes, variables, psycopg2, datetime, path, debug, traceback

from typing import Any, Literal, Tuple


def connect() -> Tuple[Any, Any] or Tuple[Literal[False], Literal[False]]:
    """
    This definition returns connection to database.
    """
    try:
        connect = psycopg2.connect(database = 'postgres' ,
                                   password = '111' ,
                                   user     = 'postgres' ,
                                   host     = '127.0.0.1',
                                   port     = '5432'     )        
        
        return connect, connect.cursor()
    
    except:
        debug.saveLogs(f'------ERROR!------\n\n{traceback.format_exc()}', path.log_file)
    
    return (False, False)


def insert_message(user_id, oper_id, text = 'TEXT DATABASE', status = 'open') -> bool or str:
    """
    This definition connect user and operator in database.

    params:
           user_id : int
           oper_id : int

    To create table use:
    CREATE TABLE message_tb(id serial primary key, user_id INTEGER        , 
                            oper_id INTEGER      , date_start VARCHAR(255), 
                            text TEXT            , status VARCHAR(255)    );
    """
    con, cur = connect()
    if con and cur:
        try:
            if not oper_id:

                cur.execute("INSERT INTO message_tb (date_start, user_id, oper_id, text, status) "
                            f"VALUES ('{datetime.date.today().timetuple()[0:3]}', "
                            f"         {user_id}, {oper_id}, '{text}', '{status}')")

                con.commit()
                return True

            elif user_id and oper_id:
            
                cur.execute(f"UPDATE message_tb          SET oper_id = {oper_id},   "
                            f"text =   '{text}\nOper: {oper_id}\nUser: {user_id}\n' " 
                            f"WHERE  status = '{status}' AND user_id = {user_id};   "
                             "SELECT id         FROM      message_tb    WHERE       "
                            f"       status = '{status}' AND user_id = {user_id}    ")
                
                text = f'#id Переписки: {cur.fetchall()[0][0]}'
                con.commit()
                return text

        except:
            debug.saveLogs(f'------ERROR!------\n\n{traceback.format_exc()}', path.log_file)
    
    return False

def insert_feedback(oper_id, user_id, text, status = 'open') -> str or Literal[False]:
    con, cur = connect()
    if con and cur:
        try:
            if not oper_id and user_id:
                
                cur.execute( "INSERT                INTO              feedback_tb  "
                             "(user_id,  oper_id,  text_fb,  status,  date_enter)  "
                            f"VALUES ({user_id}, {oper_id}, '{text}', '{status}',  "
                            f"       '{datetime.date.today().timetuple()[0:3] }'); "
                            f"SELECT id FROM feedback_tb WHERE status = '{status }'" 
                            f"                           AND  user_id =  {user_id} ")

                text = f'#id Жалобы: {cur.fetchall()[0][0]}'
                con.commit()
                return text

            else:

                cur.execute(f"SELECT text_fb FROM feedback_tb WHERE status = '{status }' "
                            f"                                AND  user_id =  {user_id}; "
                            f"UPDATE              feedback_tb SET  oper_id =  {oper_id}, "
                            f"text_fb = 'TEXT FEEDBACK\n"
                                       f"{cur.fetchall()[0][0]}\n"
                                       f"Operator: {oper_id}\n"
                                       f"Текст: {text}'    "
                            f"WHERE  status = '{status}' AND  user_id =  {user_id}; "
                            f"SELECT id FROM feedback_tb WHERE status = '{status }' "
                            f"                           AND  user_id =  {user_id}  ")
 
                text = f'#id Жалобы: {cur.fetchall()[0][0]}'
                
                cur.execute( "UPDATE feedback_tb SET status = 'close' WHERE "
                            f"status = '{status}' AND user_id = {user_id}   ")
                
                con.commit()
                return text
        
        except:
            debug.saveLogs(f'------ERROR!------\n\n{traceback.format_exc()}', path.log_file)
        
    return False

def insert_text(text, id, status = 'open') -> bool:
    con, cur = connect()
    if con and cur:
        try:

            cur.execute( "SELECT text FROM message_tb WHERE status = '{status}' "
                        f"AND    (oper_id = {id}      OR   user_id =  {id}   ); "
                        f"UPDATE message_tb SET text = '{cur.fetchall()[0][0]}\n{text}'   "
                        f"WHERE status = '{status}' AND (user_id = {id} OR oper_id = {id})")

            con.commit()
            return True

        except:
            debug.saveLogs(f'------ERROR!------\n\n{traceback.format_exc()}', path.log_file)

    return False

def closerDataBase(id, status = 'open', set = 'close') -> bool:
    con, cur = connect()
    if con and cur:
        try:

            cur.execute( "SELECT user_id, oper_id FROM message_tb WHERE status = '{status}' "
                        f"AND (oper_id = {id} OR user_id = {id})")

            user_id, oper_id = cur.fetchall()[0][:2]

            if user_id and oper_id:
                cur.execute(f"UPDATE message_tb SET status = '{set}' WHERE status = '{status}' "
                            f"AND user_id = {id} OR oper_id = {id}                             ")
            else:
                cur.execute(f"DELETE FROM message_tb WHERE status = '{status}' "
                            f"AND (oper_id = {id} OR user_id = {id})           ")

            con.commit()
            return True

        except:
            debug.saveLogs(f'------ERROR!------\n\n{traceback.format_exc()}', path.log_file)
    
    return False


### For message_tb and feedback_tb

def getDataFromDB(date_start, action, row_dict = {'message_tb'  : 'date_start', 
                                                  'feedback_tb' : 'date_enter'} ):
    con, cur = connect()
    if con and cur:
        try:
            accounts = get_accounts_data()

            cur.execute(f"SELECT id, user_id FROM {action} WHERE {row_dict[action]} = '{date_start}'")

            db_accounts = cur.fetchall()

            text_adder = 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n'
            
            for i in db_accounts:
                for k in accounts:
                    if k == str(i[1]):
                        name_id = f"@{accounts[k].login}" if accounts[k].login != 'None' else accounts[k].name
                        break
                text_adder = f"{text_adder}{str(i[0])}) Name: {name_id} --- Id: {str(i[1])}\n"
            con.commit()
            return text_adder if text_adder != 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n' else False
        except:
            debug.saveLogs(f'------ERROR!------\n\n{traceback.format_exc()}', path.log_file)

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
            if   action == 'take_id': text_commmit = 'SELECT message_id FROM messageId_tb'
            elif action == 'save_id': text_commmit = f'UPDATE messageId_tb set message_id = {message_id}'
            elif action == 'init_id': text_commmit = f'INSERT INTO messageId_tb (message_id) VALUES ({message_id})'
            cur.execute(text_commmit)
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


### Unit test for database.py

def test_database() -> bool:
    
    test_connect, _ = connect()
    debug.saveLogs(f'DB_CONNECTION [{True if test_connect else False}] <- connect()\n\n', path.log_file)

    test_insert_data = insert_message(8881, 0)
    debug.saveLogs(f'DB_INSERT_1 [{True if test_insert_data else False}] <- connect()\n\n', path.log_file)

    test_insert_data = insert_message(8881, 8882)
    debug.saveLogs(f'DB_INSERT_2 [{True if test_insert_data else False}] <- connect()\n\n', path.log_file)


if __name__ == "__main__":
    test_database()


    