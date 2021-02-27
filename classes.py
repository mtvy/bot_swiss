from lib import *

class Account:

    def __init__(self, acc):
        self.telegram_id = acc[0]
        self.login = acc[1]
        self.name = acc[2]
        self.oper_ids = acc[3]
        self.conversation = acc[4]
        self.discount = acc[5]
        self.tags = acc[6]
        self.ref = acc[7]
        self.personal_data = acc[8]
        self.language = acc[9]
        self.feedback_st = acc[10]
        self.timer_conv = acc[11]
    
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
    acc = database.get_accounts_data()
    for i in acc.keys(): print(acc[i])
if __name__ == '__main__':
    read()