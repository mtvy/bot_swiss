"""
Postgresql database processor.
"""
import debug             ,\
       utility   as ut   ,\
       variables as var  ,\
       psycopg2  as psql ,\
       traceback as error

from classes import *

from datetime import date
from typing   import Any, Dict, Literal, Tuple

CONN_ADRGS = {
    'database' : 'postgres' ,
    'password' : 'postgres' ,
    'user'     : 'postgres' ,
    'host'     : 'postgres',
    'port'     : '5433'     
}


def connect() -> Tuple[Any, Any] or Tuple[Literal[False], Literal[False]]:
    """
    This definition returns connection to database.
    """
    try:
        con = psql.connect(**CONN_ADRGS)        
        
        return con, con.cursor()
    
    except:
        debug.saveLogs(f'[connect]---->{error.format_exc()}')
    
    return (False, False)


def __is_exist(cur, tb : str, status : str, _id : str, t_id : str) -> bool:
    try:
        cur.execute(
            f'SELECT id FROM {tb} WHERE  '
            f'status      = \'{status}\' '
            f'AND {t_id} = \'{_id}\'     '
        )
        return bool(cur.fetchall())
    except:
        debug.saveLogs(f'[__is_exist]---->{error.format_exc()}')

    return False

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
            is_id = not __is_exist(cur, 'message_tb', 
                status, user_id, 'user_id'
            )
            
            if not oper_id or is_id:
                
                _date = date.today().timetuple()[0:3]
                _date = f'{_date[0]}-{_date[1]}-{_date[2]}'
                    
                cur.execute(
                    'INSERT INTO message_tb (  '
                    '   date_start            ,'   
                    '   user_id               ,'
                    '   oper_id               ,'
                    '   text                  ,'
                    '   status                 '
                    ') VALUES (                '
                   f'    \'{_date}\'  , {user_id} ,'
                   f'    {oper_id}, \'{text}\','
                   f'    \'{status}\'              '
                   ')                          '
                )

                con.commit()
                if not is_id: return True

            if user_id and oper_id:
            
                cur.execute(f"UPDATE message_tb          SET oper_id = '{oper_id}',   "
                            f"text =   '{text}\nOper: {oper_id}\nUser: {user_id}\n' " 
                            f"WHERE  status = '{status}' AND user_id = '{user_id}';   "
                             "SELECT id         FROM      message_tb    WHERE       "
                            f"       status = '{status}' AND user_id = '{user_id}'    ")
                
                text = f'#id Переписки: {cur.fetchall()[0][0]}'
                con.commit()
                return text

        except:
            debug.saveLogs(f'[insert_message]---->{error.format_exc()}')
    
    return False

def insert_feedback(oper_id, user_id, text, status = 'open') -> str or Literal[False]:
    con, cur = connect()
    if con and cur:
        try:
            if not oper_id and user_id:
                
                cur.execute( "INSERT                INTO              feedback_tb  "
                             "(user_id,  oper_id,  text_fb,  status,  date_enter)  "
                            f"VALUES ({user_id}, {oper_id}, '{text}', '{status}',  "
                            f"       '{date.today().timetuple()[0:3] }'); "
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
            debug.saveLogs(f'------ERROR!------\n\n{error.format_exc()}')
        
    return False

def insert_text(text, id, status = 'open') -> bool:
    con, cur = connect()
    if con and cur:
        try:

            cur.execute(
                f"SELECT text FROM message_tb WHERE status = '{status}' "
                f"AND (oper_id = '{id}' OR user_id = '{id}')           ;"
            )
            cur.execute(
                f"UPDATE message_tb SET text = '{cur.fetchall()[0][0]}\n{text}' "
                f"WHERE status = '{status}' AND (user_id = '{id}' OR oper_id = '{id}')"
            )
            con.commit()
            return True

        except:
            debug.saveLogs(f'[insert_text]---->{error.format_exc()}')

    return False

def change_status(_id, status = 'open', _set = 'close') -> bool:
    con, cur = connect()
    if con and cur:
        try:
            is_id = __is_exist(cur, 'message_tb', 
                status, _id, 'user_id'
            )

            if not is_id:
                is_id = __is_exist(cur, 'message_tb', 
                    status, _id, 'oper_id'
                )

            if is_id:
                cur.execute(
                     'SELECT user_id, oper_id FROM message_tb     '
                    f"WHERE status = '{status}'                   "
                    f"AND (oper_id = '{_id}' OR user_id = '{_id}')"
                )

                user_id, oper_id = map(int, cur.fetchall()[0][:2])

                if user_id and oper_id:
                    cur.execute(
                        f"UPDATE message_tb SET status = '{_set}'    "
                        f"WHERE status = '{status}'                  "
                        f"AND (user_id = '{_id}' OR oper_id = '{_id}')"
                    )
                else:
                    cur.execute(
                         'DELETE FROM message_tb    '
                        f"WHERE status = '{status}' "
                        f"AND (oper_id = '{_id}'    "
                        f"  OR user_id = '{_id}')   "
                    )

            con.commit()

            return True

        except:
            debug.saveLogs(f'[change_status]---->{error.format_exc()}')
    
    return False


### For message_tb and feedback_tb

def get_data(dating : str, 
             action : str, 
             text : str =  'ID ПОЛЬЗОВАТЕЛЕЙ\n\n', 
             row  : Dict[str, str] = {'message_tb'  : 'date_start', 
                                      'feedback_tb' : 'date_enter'} ) -> str or bool:
    con, cur = connect()
    if con and cur:
        try:

            accs = get_accounts()

            cur.execute(f"SELECT id, user_id FROM {action} WHERE {row[action]} = '{dating}'")

            db_accs = cur.fetchall()
            
            for db_acc in db_accs:
                for acc in accs:
                    if acc == db_acc[1]:
                        name_id = (f"@{accs[acc].login}" if   accs[acc].login != None 
                                                                 else accs[acc].name)
                        text = f"{text}{db_acc[0]}) Name: {name_id} --- Id: {db_acc[1]}\n"
                        break

            con.commit()
            return text if text != 'ID ПОЛЬЗОВАТЕЛЕЙ\n\n' else False

        except psql.errors.UndefinedTable as ex:
            debug.saveLogs(f'[get_accounts][{action}]---->{ex}')
            
            create_db(
                'CREATE TABLE feedback_tb(    '
                '    id serial primary key   ,' 
                '    oper_id varchar(15)     ,'
                '    user_id varchar(15)     ,'
                '    date_enter varchar(255) ,' 
                '    text_fb text            ,'
                '    status varchar(255)      '
                ');' if action == 'feedback_tb' else
                'CREATE TABLE message_tb(     '
                '    id serial primary key   ,'
                '    oper_id varchar(15)     ,'
                '    user_id varchar(15)     ,'
                '    date_start varchar(255) ,'
                '    text text               ,'
                '    status varchar(255)      '
                ');                           '
            )

        except:
            debug.saveLogs(f'------ERROR!------\n\n{error.format_exc()}')

    return False

def get_text(id, action, row = {'message_tb' : 'text', 'feedback_tb' : 'text_fb'}):
    con, cur = connect()
    if con and cur:
        try:

            cur.execute(f"SELECT {row[action]} FROM {action} WHERE id = {id}")

            con.commit()
            return cur.fetchall()[0][0]

        except:
            debug.saveLogs(f'------ERROR!------\n\n{error.format_exc()}')
    
    return False


### For collection

def check_pull(cur, action = None, step = None) -> Any or bool:
    return cur.fetchall() if action == 'show_data' or step == 9 else True

def dbCollection(message, id, **kwargs) -> Any or bool:
    """
    To create table: 
    CREATE TABLE collection_tb(id serial primary key         , 
                               admin_id         VARCHAR(128) , 
                               cashier_id       VARCHAR(128) , 
                               office           VARCHAR(128) , 
                               terminal_number  TEXT         , 
                               cash             TEXT         , 
                               cash_return_info TEXT         , 
                               doc_number       TEXT         , 
                               PCR              TEXT         , 
                               PCR_express      TEXT         , 
                               analyzes_count   TEXT         , 
                               comment          TEXT         , 
                               admin_date       VARCHAR(128) , 
                               cashier_date     VARCHAR(128) , 
                               status           VARCHAR(128) );
    """
    con, cur = connect()
    if con and cur:
        try:
            if 'step' in kwargs and (not kwargs['step']):

                text = ( "INSERT INTO collection_tb (admin_id  , office, "
                         "                           admin_date, status) "
                        f"VALUES                    ('{id            }', "
                        f"                           '{message.text  }', "
                        f"                           '{date.today()  }', "
                        f"                           'admin'           ) ")

            elif kwargs['action'] == 'cashier_init':

                text = (f"UPDATE collection_tb SET cashier_id = '{id                 }' "
                        f"WHERE                        office = '{kwargs['push_data']}' "
                        f"AND                          status = 'cashier'               ")

            elif kwargs['step'] in [1,2,3,4,5,6,7,8] and kwargs['action'] == 'show_data':

                action = var.collection_actions[kwargs['step']]
                set    = ut.takeFilled(kwargs['push_data'], message.text)

                text   = (f"UPDATE collection_tb SET {action}   = '{set}'     "
                          f"WHERE                   (admin_id   = '{id}'     "
                          f"AND                      status     = 'admin')    "
                          f"OR                      (cashier_id = '{id}'     "
                          f"AND                      status     = 'cashier'); "
                          f"SELECT * FROM collection_tb                     "
                          f"WHERE                   (admin_id   = '{id}'      "
                          f"AND                      status     = 'admin')    "
                          f"OR                      (cashier_id = '{id}'     "
                          f"AND                      status     = 'cashier') ")
            
            elif kwargs['step'] in [1,2,3,4,5,6,7,8]:

                action = var.collection_actions[kwargs['step']]
                set    = ut.takeFilled(kwargs['push_data'], message.text)

                text = (f"UPDATE collection_tb SET {action} = '{set}' "
                        f"WHERE                    admin_id = '{id}'  "
                        f"AND                        status = 'admin' ")
            
            elif kwargs['action'] == 'send_collection_to_oper':

                text = (f"UPDATE collection_tb SET status = 'cashier' "
                        f"WHERE                    status = 'admin'   "
                        f"AND                    admin_id = '{id}'    ")
                
            elif kwargs['action'] == 'confirm_collection':

                text = (f"UPDATE collection_tb SET status = 'confirmed' "
                        f"WHERE                    status = 'cashier'   "
                        f"AND                  cashier_id = '{id}'      ")

            elif kwargs['action'] == 'show_collection_to_cashier':

                text = (f"SELECT * FROM collection_tb WHERE status = 'cashier'              "
                        f"AND                               office = '{kwargs['push_data']}'")
                
            elif kwargs['step'] == 9:

                text = (f"SELECT * FROM collection_tb WHERE status = '{kwargs['push_data']}' "
                        f"AND                            (admin_id = '{id}'                  "
                        f"OR                            cashier_id = '{id}')                 ")
            
            cur.execute(text)

            data = check_pull(cur = cur, action = kwargs['action'], step = kwargs['step'])

            con.commit()
            return data

        except:
            debug.saveLogs(f'------ERROR!------\n\n{error.format_exc()}')
    
    return False


### For check MESSAGE_ID

def dbMessageId(action, message_id = None) -> Any or bool:
    """
    This definition handles id of posting message.

    To create table: 
    CREATE TABLE messageId_tb(message_id INTEGER);
    """
    con, cur = connect()
    if con and cur:
        try:
            COMMANDS_MOD = {
                'take_id' : 'SELECT message_id FROM messageId_tb',
                'save_id' : f'UPDATE messageId_tb SET message_id = {message_id}',
                'init_id' : f'INSERT INTO messageId_tb (message_id) VALUES ({message_id})'
            }

            cur.execute(COMMANDS_MOD[action])

            data = check_pull(cur = cur, action = 'show_data' if action == 'take_id' else None)

            con.commit()
            return data

        except psql.errors.UndefinedTable as ex:
            debug.saveLogs(f'[dbMessageId][messageId_tb]---->{ex}')

            create_db(
                'CREATE TABLE messageId_tb(message_id INTEGER);'
            )

        except:
            debug.saveLogs(f'[dbMessageId]---->{error.format_exc()}')
    
    return False


### For account_tb

def insert_account(acc : Account) -> bool:
    """
    This definition inserts an Account class object into the database.
    """
    con, cur = connect()
    if con and cur:
        try:
            cur.execute( 'INSERT INTO account_tb (telegram_id  , login     ,     '
                         '                        name         , oper_ids  ,     '
                         '                        conversation , discount  ,     '
                         '                        tags         , ref       ,     '
                         '                        personal_data, language  ,     '
                         '                        feedback_st  , timer_conv)     '
                         'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'     , 
                         (acc.telegram_id, acc.login   , acc.name       , acc.oper_ids  , 
                          acc.conversation, acc.discount, acc.tags       , acc.ref       , 
                          acc.personal_data, acc.language, acc.feedback_st, acc.timer_conv)
            )

            con.commit()
            return True

        except:
            debug.saveLogs(f'------ERROR!------\n\n{error.format_exc()}')
    
    return False

def update_account(acc : Account , param, data) -> bool:
    """
    This definition updates an Account class object in the database.
    """
    con, cur = connect()
    if con and cur:
        try:

            cur.execute(f'UPDATE account_tb SET {param}'' = %s '
                         'WHERE               telegram_id = %s ', 
                        (data, acc.telegram_id)
            )
            
            con.commit()
            return True

        except:
            debug.saveLogs(f'------ERROR!------\n\n{error.format_exc()}')
    
    return False

def get_accounts(accounts : Dict = {}, attr = 'telegram_id') -> Dict[int, Account]:
    """
    This definition gets an Account class object from the database.
    """
    con, cur = connect()
    if con and cur:
        try:
            cur.execute("SELECT telegram_id  , login     , "
                        "       name         , oper_ids  , "
                        "       conversation , discount  , "
                        "       tags         , ref       , "
                        "       personal_data, language  , "
                        "       feedback_st  , timer_conv  "
                        "FROM   account_tb                 ")

            for account in cur.fetchall():
                accounts = ut.takeClassDict(inst = Account(account), 
                                            attr = attr                , 
                                            var  = accounts            )

            con.commit()
            return accounts

        except psql.errors.UndefinedTable as ex:
            debug.saveLogs(f'[get_accounts][account_tb]---->{ex}')

            create_db(
                'CREATE TABLE account_tb(           '
                '       id serial primary key     , '
                '       telegram_id varchar(255)  , '
                '       login varchar(255)        , '
                '       name varchar(255)         , '
                '       oper_ids varchar(10)[]    , '
                '       conversation varchar(255) , '
                '       discount varchar(255)     , '
                '       tags varchar(10)[]        , '
                '       ref varchar(255)          , '
                '       personal_data varchar(255), '
                '       language varchar(255)     , '
                '       feedback_st varchar(255)  , '
                '       timer_conv integer          '
                ');                                 '
            )
        
        except:
            debug.saveLogs(f'[get_accounts]---->{error.format_exc()}')
    
    return {}


def create_db(com : str) -> bool:
    """
    """
    con, cur = connect()
    if con and cur:
        try:
            cur.execute(com)
            con.commit()
            return True
        except:
            debug.saveLogs(f'[create_db]---->{error.format_exc()}')
    
    return False


### Unit test for database.py

def __test_database() -> bool:
    
    test_connect, _ = connect()
    debug.saveLogs(f'DB_CONNECTION [{True if test_connect else False}] <- connect()\n\n')

    test_insert_data = insert_message(8881, 0)
    debug.saveLogs(f'DB_INSERT_1 [{True if test_insert_data else False}] <- connect()\n\n')

    test_insert_data = insert_message(8881, 8882)
    debug.saveLogs(f'DB_INSERT_2 [{True if test_insert_data else False}] <- connect()\n\n')


if __name__ == "__main__":
    #dbMessageId('init_id', int(input()))
    #dbMessageId('init_id', int(input()))
    __test_database()
    
    
    #acc = database.get_accounts_data()
    #for i in acc.keys(): print(acc[i], '\n')


    