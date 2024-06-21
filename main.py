import requests
import json
import gspread
import badminton
import line_server
import logger
# ====================================================
sheet_admin = None
sheet_admin_data_list = None
badminton_param = None
badminton_param_data_list = None
line_param = None
line_param_data_list = None
cmd_param = None
cmd_param_data_list = None
# 取得googlesheet資料==================================
logger.print("開始讀取 google sheet...")
try:
    gc = gspread.service_account(
        filename='./authorize/badminton-426909-fa7d76bbe33e.json')
    sheet = gc.open('羽球小幫手')

    sheet_admin = sheet.worksheet("管理員")
    sheet_admin_data_list = sheet_admin.get_all_records(False, 1, "", True)

    badminton_param = sheet.worksheet("羽球參數")
    badminton_param_data_list = badminton_param.get_all_records(
        False, 1, "", True)

    line_param = sheet.worksheet("LINE參數")
    line_param_data_list = line_param.get_all_records(
        False, 1, "", False)

    cmd_param = sheet.worksheet("指令參數")
    cmd_param_data_list = cmd_param.get_all_records(
        False, 1, "", False)
except Exception as e:
    logger.print("讀取 sheet_data 失敗\n" + str(e))

logger.print("google sheet讀取完成")
badminton.init(sheet_admin_data_list,
               badminton_param_data_list,  cmd_param_data_list)

line_server.run(line_param_data_list)
