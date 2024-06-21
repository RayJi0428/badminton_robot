# https://levelup.gitconnected.com/google-sheet-api-and-python-af188b3cf894
# 要先到google cloud platfrom建立專案
# 啟用Google Drive API & Google Sheets API
# https://console.cloud.google.com/
# API和服務>憑證>建立憑證>精靈>
# (Google Sheets API/其他介面/應用程式資料)>隨便服務名稱(ray)>角色(Project Editor)>金鑰類型(json)
# 建立憑證後存為json(creds.json)
# creds.json內有client_email
# 找到要存取的表單分享給client_email使用者
# 如果未安裝gspread，則需要先安裝它
# pip install gspread oauth2client
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# sample1(run不起來)------------------------------------------------------------------
# scope = ["https://spreadsheets.google.com/feeds",
#          "https://googleapis.com/auth/spreadsheets",
#          "https://www.googleapis.com/auth/drive.file",
#          "https://www.googleapis.com/auth/drive"]

# creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
# client = gspread.authorize(creds)
# sheet = client.open("test").sheet1
# data = sheet.get_all_records()
# print(data)

# sample2(OK)------------------------------------------------------------------

# global
sheet_instance = None


def load(credsJson, titleName, sheetName, headRow):
    global sheet_instance
    print("開始讀取 google sheet...")
    try:
        gc = gspread.service_account(filename=credsJson)
        # extract data from google sheet by the name of the sheet\
        # 文件名稱
        sheet = gc.open(titleName)
        # For the first sheet, pass the index 0 and so on.
        # 分頁名稱
        sheet_instance = sheet.worksheet(sheetName)
        # get all the records of the data
        # sheet_data = sheet_instance.get_all_records(False, headRow, "", True) 最後一個True不知道作用, 會導致_被吃掉
        sheet_data = sheet_instance.get_all_records(False, headRow, "", False)
    except Exception as e:
        print("讀取 sheet_data 失敗\n" + str(e))
    return sheet_data


print("google sheet 讀取完成")


def gs_to_df(creds_file, sheet_name, head=1):
    # Read Data from a Spreadsheet
    # gspread – to interact with Google Spreadsheets
    gc = gspread.service_account(filename=creds_file)
    # extract data from google sheet by the name of the sheet
    sheet = gc.open(sheet_name)
    # For the first sheet, pass the index 0 and so on.
    sheet_instance = sheet.get_worksheet(0)
    # get all the records of the data
    records_data = sheet_instance.get_all_records(False, head)
    # convert the json to dataframe
    # df = pd.DataFrame(records_data)
    return records_data

# 使用get_all_records數字無法視為字串使用(ex:0050會被視為50)，可用get_all_values自行處理解決


def gs_get_all_values(creds_file, sheet_name, head=1):
    # Read Data from a Spreadsheet
    # gspread – to interact with Google Spreadsheets
    gc = gspread.service_account(filename=creds_file)
    # extract data from google sheet by the name of the sheet
    sheet = gc.open(sheet_name)
    # For the first sheet, pass the index 0 and so on.
    sheet_instance = sheet.get_worksheet(0)
    # get all the records of the data
    records_data = sheet_instance.get_all_values()
    # convert the json to dataframe
    # df = pd.DataFrame(records_data)
    return records_data


def batch_update(data):
    global sheet_instance
    sheet_instance.batch_update(data)
