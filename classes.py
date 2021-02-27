from lib import *

class Account:

    def __init__(self, i, acc):
        self.personal_data = acc[i]['personal data']	        
        self.conversation = acc[i]['conversation']	       
        self.feedback_st = acc[i]['feedback_st']	        
        self.timer_conv = acc[i]['timer_conv']	        
        self.language = acc[i]['language']	        
        self.oper_ids = acc[i]['oper_ids']	       
        self.discount = acc[i]['discount']	
        self.login = acc[i]['login']	        
        self.name = acc[i]['name']	        
        self.tags = acc[i]['tags']	        
        self.ref = acc[i]['ref']
        self.telegram_id = str(i)
    
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
    box = [['i', Account(i, acc)] for i in acc]
    for i in box:
        print(i[1])
        database.insert_account_data(account = i[1])
       	database.change_account_data(account = i[1], parametr = "personal_data", data = "YES")
    #acc = database.get_accounts_data()
if __name__ == '__main__':
    read()
