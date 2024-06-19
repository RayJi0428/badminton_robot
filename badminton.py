import datetime
import os
global target_date

week_day_tw = ['一', '二', '三', '四', '五', '六', '日']

initialize = False
# 管理者id
admin_list = ['Ud1ed3fe766c7a88edf91e7bae56c5b1d']
# 日期
date_string = '00/00'
# 時間
time_string = '20:00-22:00'
# 星期
week_day = '-'
# 幾面場
area = '3'
# 成員清單
permanent_member_list = ['花生', '靖玟', 'ray', '盈萱',
                         '傑哥', '小彬', '子維', '仕安', 'gugu', 'ken', '曉淵', '子寧']
parttime_member_list = []
#
# --------------------------------------------------------


def is_admin(user_id):
    return user_id in admin_list


# 設定季繳成員 ex:'@季繳 花生,靖玟'
def setup_permanent_member(input_member_list):
    global permanent_member_list
    result_msg = '設定失敗'
    for member in input_member_list:
        member = member.lower()
        if member not in permanent_member_list:
            permanent_member_list.append(member)
            result_msg = '設定成功'
    return result_msg

    # 建立活動
    # 輸入規則 '@建立
    # 取資料從索引2開始


def initiate(input_date):
    global date_string
    global week_day
    global time_string
    global area
    global initialize
    initialize = True
    data_idx = 0
    # 日期
    date_string = input_date
    date_string_list = input_date.split('/')
    y = datetime.datetime.today().year
    m = date_string_list[0]
    d = date_string_list[1]
    full_date_string = f'{y}-{m}-{d}'
    date_obj = datetime.datetime.strptime(full_date_string, '%Y-%m-%d')
    week_day = date_obj.weekday()

    return get_summary()


def over():
    global initialize
    result_msg = ''
    if initialize == False:
        result_msg = '還沒開喔~~~不要急:)'
    else:
        initialize = False
        result_msg = get_summary()
        result_msg += '🈵'
    return result_msg


def intro():
    result_msg = ""\
        "/指令 (印出說明)\n" \
        "/建立 01/01 (管理員開啟活動)\n"\
        "/季繳 A,B,... (設定季繳清單)\n"\
        "/場地 3 (設定場地數)\n"\
        "/時間 20:00-22:00 (設定時間)\n"\
        "/報名 XXX (XXX報名)\n"\
        "/取消 XXX (XXX取消)\n"\
        "/查看 (印出最新資訊)"\
        ""
    return result_msg


def apply(member):
    member = member.lower()
    result_msg = '報名失敗T____T'
    if initialize == False:
        result_msg = '還沒開喔~~~不要急:)'
    else:
        if member in permanent_member_list or member in parttime_member_list:
            result_msg = '已經報了拉!是要報幾次凸'
        else:
            parttime_member_list.append(member)
            result_msg = get_summary()

    return result_msg


def cancel(member):
    member = member.lower()
    result_msg = '找不到阿...你確定你有報?凸'
    if initialize == False:
        result_msg = '還沒開取消屁?凸'
    elif member in permanent_member_list:
        permanent_member_list.remove(member)
        result_msg = get_summary()
    elif member in parttime_member_list:
        parttime_member_list.remove(member)
        result_msg = get_summary()

    return result_msg


def edit_area(input_area):
    global area
    area = input_area
    result_msg = get_summary()
    return result_msg


def edit_time(input_time):
    global time_string
    time_string = input_time
    result_msg = get_summary()
    return result_msg


def get_summary():
    # 總結
    summary_str = ''

    # 標題
    title = f'【{date_string}(週{week_day_tw[week_day]})崇德大都會】\n{time_string} {area}面場'
    summary_str += title + '\n'

    # 成員
    seat_count = int(area) * 8
    mem_str = ''
    mem_idx = 1
    # 季繳
    for permanent_member in permanent_member_list:
        mem_str += f'{mem_idx}.{permanent_member}\n'
        mem_idx += 1
    # 零打
    for partime_member in parttime_member_list:
        mem_str += f'{mem_idx}.{partime_member}(零打)\n'
        mem_idx += 1
    # 空位
    if mem_idx < seat_count:
        for i in range(mem_idx, (seat_count+1)):
            mem_str += f'{mem_idx}.\n'
            mem_idx += 1
    summary_str += mem_str

    print(summary_str)
    write(summary_str)

    return summary_str


def write(input_log):
    today = datetime.datetime.today()
    log_path = f'log/{today.date()}-log.txt'
    log = ''
    with open(log_path, mode='r') as f:
        log = f.read()

    log += f'{today}:{input_log}\n'
    with open(log_path, mode='w') as f:
        f.write(log)
        f.close()
