import logger
# 取得參數


def get_param_by_key(list, key):
    value = None
    for param_data in list:
        if param_data['名稱'] == key:
            value = param_data['參數']
            break
    if value == None:
        logger.print(f'找不到參數{key}')
    else:
        return value
