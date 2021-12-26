import path, datetime

def saveLogs(text) -> int:
    text = f'\nDate: {datetime.date.ctime}\n {text}'
    return open(path.log_file, 'w+', encoding='utf-8').write(f'\nDate: {datetime.date.ctime}\n'
                                                             f'\n      {text}')





