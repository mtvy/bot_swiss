import path, datetime

def saveLogs(text, log_file) -> int:
    return open(log_file, 'a', encoding='utf-8').write(f'\nDate: {datetime.datetime.now()}\n'
                                                        f'\n      {text}')





