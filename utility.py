from typing import Any, ClassVar, Dict

def saveText(text, file, mode, encoding = 'utf-8') -> int:
    return open(file = file, mode = mode, encoding = encoding).write(text)

def takeFilled(*args) -> Any or None:
    return [var for var in args if var]

def takeClassDict(inst, attr : str, var : Dict = {}) -> Dict:
    return {**var , getattr(inst, attr) : inst}