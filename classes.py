from lib import *

class Account:

    def __init__(self, acc):
        self.telegram_id = acc[0]
        self.personal_data = acc[1]
        self.conversation = acc[2]
        self.feedback_st = acc[3]
        self.timer_conv = acc[4]
        self.language = acc[5]
        self.oper_ids = acc[6]
        self.discount = acc[7]
        self.login = acc[8]
        self.name = acc[9]
        self.tags = acc[10]
        self.ref = acc[11]
    
    def __str__(self):
        return str({
            'telegram_id': self.telegram_id,
            'login': self.login,
            'name':  self.name,
            'oper_ids':  self.oper_ids,
            'conversation': self.conversation,
            'discount':  self.discount,
            'tags': self.tags,
            'ref':  self.ref,
            'personal_data': self.personal_data,
            'language': self.language,
            'feedback_st': self.feedback_st,
            'timer_conv': self.timer_conv,
        })

        
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
        
def read():
    acc = openfileforRead('set')
    box = [['i', Account(acc)] for i in acc]
    for i in box:
        print(i[1])
        database.insert_account_data(account = i[1])
       	database.change_account_data(account = i[1], parametr = "personal_data", data = "YES")
    
if __name__ == '__main__':
    read()
