from lib import *

class Account:

    def __init__(self, i, acc):
        self.personal_data = acc[i]['personal data']
        self.conversation = acc[i]['conversation']
        #self.feedback_st = acc[i]['feedback_st']
        self.language = acc[i]['language']
        self.oper_ids = acc[i]['oper_ids']
        self.discount = acc[i]['discount']
        #self.timer = acc[i]['timer_conv']
        self.login = acc[i]['login']
        self.name = acc[i]['name']
        self.tags = acc[i]['tags']
        self.ref = acc[i]['ref']
    
    def __str__(self):
        return str({
            'login': self.login,
            'name':  self.name,
            'oper_ids':  self.oper_ids,
            'conversation': self.conversation,
            'discount':  self.discount,
            'tags': self.tags,
            'ref':  self.ref,
            'personal data': self.personal_data,
            'language': self.language,
            #'feedback_st': self.feedback_st,
            #'timer_conv': self.timer,
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
    box = [['i', Account(i,acc)] for i in acc]
    for i in box:
        print(i[1])
if __name__ == '__main__':
    read()