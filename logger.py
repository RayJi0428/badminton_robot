import datetime
import os


def print(str, write=True):
    today = datetime.datetime.today()
    log_str = f'{today}:{str}'

    # 要寫到文字檔
    if write == True:
        log_path = f'log/{today.date()}-log.txt'
        log = ''

        # 檔案存在先取得原log
        if os.path.exists(log_path) == True:
            with open(log_path, mode='r', encoding='utf-8') as f:
                log = f.read()

        log += f'{log_str}\n'
        with open(log_path, mode='w', encoding='utf-8') as f:
            f.write(log)
            f.close()
