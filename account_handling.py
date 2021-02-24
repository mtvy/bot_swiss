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
    elif action == 'r':
        with open(path_acc_settings, 'r') as file_set:
            if(file_set.readline() == ""): 
                account_settings = {}
            else:
                file_set.close()
                with open(path_acc_settings, 'r') as file_set:
                    account_settings = json.load(file_set)
    elif action == 'w+':
        with open(path_acc_settings, 'w+') as f:
            json.dump(account_settings, f, indent='    ')
    else:
        file_text = ''
        with io.open(name_path, encoding='utf-8') as file_set:
                        for i in file_set:
                            file_text += i
        return file_text
        
        
def 
