from flask import Flask, request, abort
import flex
import badminton
import utils
import logger
import re
from data import ResultData
# 關閉相關
import atexit
import signal
import sys
import datetime
import threading
import time

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
    Emoji,
    StickerMessage,  # 貼圖
    ImageMessage,  # 圖片
    LocationMessage,  # 地點
    Template,
    TemplateMessage,  # 選單
    FlexMessage,
    FlexContainer
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)


configuration = None  # YOUR_CHANNEL_ACCESS_TOKEN
handler = None  # YOUR_CHANNEL_SECRET
line_bot_api_instance = None  # API實體生成
line_group_id = ''  # 群組ID


# 主動push訊息
def robot_push_text(text, emojis=None):
    global line_group_id
    line_bot_api_instance.push_message_with_http_info(
        PushMessageRequest(
            to=line_group_id,
            messages=[TextMessage(text=text, emojis=emojis)]
        )
    )


# 被動回應訊息
def robot_reply_text(reply_token, reply_text, emojiIds=None):
    emojis = None
    if emojiIds != None:
        emojis = get_emojis(reply_text, emojiIds)
    line_bot_api_instance.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=reply_text, emojis=emojis)]
        )
    )


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 啟動通知
def activate():
    time.sleep(1)
    today = datetime.date.today().strftime("%m/%d")
    result_data = badminton.create(today)
    robot_push_text(result_data.reply_text)


# 關閉通知
def deactivate():
    robot_push_text("<機器人關閉>")


# 啟動
def run(line_param_data_list):
    global configuration, handler, line_bot_api_instance, line_group_id

    access_token = utils.get_param_by_key(
        line_param_data_list, 'LINE_ACCESS_TOKEN')
    line_group_id = utils.get_param_by_key(
        line_param_data_list, 'LINE_GROUP_ID')
    channel_secret = utils.get_param_by_key(
        line_param_data_list, 'LINE_CHANNEL_SECRET')

    configuration = Configuration(access_token=access_token)
    handler = WebhookHandler(channel_secret)
    line_bot_api_instance = MessagingApi(ApiClient(configuration))

    # handler定義
    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_message(event):
        try:
            with ApiClient(configuration) as api_client:
                user_id = event.source.user_id
                msg_text = event.message.text
                reply_token = event.reply_token
                print(f'user:{user_id}, msg:{msg_text}, token:{reply_token}')

                # 指令檢查----------------------------------------------
                # 指令檢查----------------------------------------------
                # 指令檢查----------------------------------------------
                cmd_data = badminton.find_cmd_in_msg(msg_text)
                # 不是指令直接忽略
                if cmd_data == None:
                    if msg_text[0] == '/' and msg_text[1] == " ":
                        robot_reply_text(
                            reply_token, '要下指令嗎？斜線和指令中間不能有空格$', ['164'])
                    elif msg_text[0] == '/':
                        robot_reply_text(
                            reply_token, '目前沒這功能喔...敬請期待$', ['171'])
                    print(f'忽略 {msg_text}')
                    return

                # admin指令權限檢查
                if cmd_data['管理員限定'] != '' and badminton.is_admin(user_id) == False:
                    robot_reply_text(reply_token, '關你屁事?$', ["169"])
                    return

                # 空格檢查
                if cmd_data['要空格'] != '':
                    msg_copy = msg_text.replace(cmd_data['KEY'], '')
                    if msg_copy[0] != ' ':
                        robot_reply_text(reply_token, '指令後面缺少空格$', ['164'])
                        return
                # 指令處理----------------------------------------------
                # 指令處理----------------------------------------------
                # 指令處理----------------------------------------------
                result_data = badminton.call_cmd_fn(
                    cmd_data['function'], event)
                # 回應文字
                if result_data.reply_text != None:
                    robot_reply_text(
                        reply_token, result_data.reply_text, result_data.reply_emojiIds)
                elif result_data.reply_image != None:
                    robot_reply_image(reply_token, result_data.reply_image)
        except Exception as e:
            robot_reply_text(reply_token, f'發生錯誤:{e.args[0]}$', ["182"])
            logger.print(e.args[0])

    # 啟動server
    # atexit.register(deactivate)
    threading.Thread(target=activate).start()
    app.run()


def find_all_hash_indexes(pattern, text):
    # 用正则表达式找出所有 '$' 的索引
    return [m.start() for m in re.finditer(pattern, text)]


# 目前一定要用$來替換!$$$很重要
# https://www.evanlin.com/line-emoji/
# "hello$" emoji索引為5
# 表情編號
# https://developers.line.biz/en/docs/messaging-api/emoji-list/#line-emoji-definitions
def get_emojis(msg_text: str, p_emojiIds):
    emojis = []
    emojiIds = p_emojiIds.copy()
    # $在正則是特殊字符,必須用\轉譯
    idx_list = find_all_hash_indexes('\$', msg_text)
    if len(idx_list) == 0:
        print('缺少特殊字符!!!!')
        emojis = None
    for idx in idx_list:
        emojis.append(
            Emoji(index=idx, productId="5ac1bfd5040ab15980c9b435", emojiId=emojiIds.pop(0)))
    return emojis


# 回傳圖片
def robot_reply_image(reply_token: str, img_url: str):
    line_bot_api_instance.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=reply_token,
            messages=[ImageMessage(
                originalContentUrl=img_url,
                previewImageUrl=img_url)]
        )
    )

# --------------------------------------------------
# def get_friends_list(channel_access_token):
#     headers = {
#         'Authorization': 'Bearer ' + channel_access_token
#     }
#     response = requests.get('https://api.line.me/friendship/v1/friends', headers=headers)
#     if response.status_code == 200:
#         friends_list = response.json()
#         return friends_list
#     else:
#         print("Failed to get friends list. Status code:", response.status_code)
#         return None
# # 填入你的 Channel Access Token
# friends_list = get_friends_list("pL+HNPLwoAAkMbDZkfVUGEzp+RybPauGAJfKYgcpm/imWaToHKybIXQ00TWEUOexrcHiV6P512Yjs1T/NiA2NrJseyxcnz5ckDDKiH9PYhnZ4aNHV35EI5UgZs46sLeEis6afHE4zkkTmtUEQIcVtgdB04t89/1O/w1cDnyilFU=")
# if friends_list:
#     print("Friends list:", friends_list)

# --------------------------------------------------
# elif "!!!地圖" in msg_text:
#     line_bot_api_instance.reply_message_with_http_info(
#         ReplyMessageRequest(
#             reply_token=reply_token,
#             messages=[LocationMessage(title="友間咖啡", address="403台中市西區西屯路一段160號",
#                                         latitude=24.15256749176782, longitude=120.67137125432184)]
#         )
#     )
# elif "!!!1" in msg_text:
#     bubble_string = flex.template_carousel_str
#     message = FlexMessage(
#         alt_text="hello", contents=FlexContainer.from_json(bubble_string))
#     line_bot_api_instance.reply_message_with_http_info(
#         ReplyMessageRequest(
#             reply_token=reply_token,
#             messages=[message])
#     )
