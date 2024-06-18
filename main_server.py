from flask import Flask, request, abort
import flex
import badminton

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
    TextMessage,
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

import requests

app = Flask(__name__)

# YOUR_CHANNEL_ACCESS_TOKEN
configuration = Configuration(
    access_token='GOf8qHpCZVsFB9MHJAw52nCsRV4JW66vmXRBiEHmj+EGYiVXu21iaSwZOyKHXmcR7xWjdY5n506izX9C7193xB6IMZkGQ79WkEjV473eapC6cl7LhyZX5fSoVU643V7rxUUTwoePGBW9IqDl4s8xoQdB04t89/1O/w1cDnyilFU=')
# YOUR_CHANNEL_SECRET
handler = WebhookHandler('de53200548c6a61f2ec66cb07f4fc123')

# API實體生成
line_bot_api_instance = MessagingApi(ApiClient(configuration))


# 簡化回應訊息
def robot_reply_text(reply_token, text):
    line_bot_api_instance.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=text)]
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


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        with ApiClient(configuration) as api_client:
            user_id = event.source.user_id
            msg_text = event.message.text
            reply_token = event.reply_token

            if "#指令" in msg_text:
                result_text = badminton.intro()
                robot_reply_text(reply_token, result_text)
            elif "#季繳" in msg_text:
                if badminton.is_admin(user_id):
                    member_list = msg_text.split(' ')[1:]
                    result_text = badminton.setup_permanent_member(member_list)
                    robot_reply_text(reply_token, result_text)
                else:
                    robot_reply_text(reply_token, '你以為你是誰?')
            elif "#建立" in msg_text:
                if badminton.is_admin(user_id):
                    date = msg_text.split(' ')[1]
                    msg_text = badminton.initiate(date)
                    robot_reply_text(reply_token, msg_text)
                else:
                    robot_reply_text(reply_token, '你以為你是誰?')
            elif "#時間" in msg_text:
                if badminton.is_admin(user_id):
                    input_time = msg_text.split(' ')[1]
                    msg_text = badminton.edit_time(input_time)
                    robot_reply_text(reply_token, msg_text)
                else:
                    robot_reply_text(reply_token, '你以為你是誰?')
            elif "#場地" in msg_text:
                if badminton.is_admin(user_id):
                    area = msg_text.split(' ')[1]
                    msg_text = badminton.edit_area(area)
                    robot_reply_text(reply_token, msg_text)
                else:
                    robot_reply_text(reply_token, '你以為你是誰?')
            elif "#報名" in msg_text:
                apply_user_data = msg_text.split(' ')
                if len(apply_user_data) == 1:
                    robot_reply_text(reply_token, '空格謝謝')
                else:
                    msg_text = badminton.apply(apply_user_data[1])
                robot_reply_text(reply_token, msg_text)
            elif "#取消" in msg_text:
                cancel_user = msg_text.split(' ')[1]
                msg_text = badminton.cancel(cancel_user)
                robot_reply_text(reply_token, msg_text)
            elif "#查看" in msg_text:
                msg_text = badminton.get_summary()
                robot_reply_text(reply_token, msg_text)
            elif "!!!貼圖" in msg_text:
                line_bot_api_instance.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[StickerMessage(
                            type="sticker", packageId="446", stickerId="1988")]
                    )
                )
            elif "!!!圖片" in msg_text:
                line_bot_api_instance.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[ImageMessage(
                            originalContentUrl="https://images.desenio.com/zoom/18197-8snoopylove50x70-79406.jpg",
                            previewImageUrl="https://images.desenio.com/zoom/18197-8snoopylove50x70-79406.jpg")]
                    )
                )
            elif "!!!地圖" in msg_text:
                line_bot_api_instance.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[LocationMessage(title="友間咖啡", address="403台中市西區西屯路一段160號",
                                                  latitude=24.15256749176782, longitude=120.67137125432184)]
                    )
                )
            elif "!!!1" in msg_text:
                bubble_string = flex.template_carousel_str
                message = FlexMessage(
                    alt_text="hello", contents=FlexContainer.from_json(bubble_string))
                line_bot_api_instance.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[message])
                )
            else:
                print(f'忽略{msg_text}')
    except Exception as e:
        robot_reply_text(reply_token, '好了吧...被你弄壞了')
        badminton.write(e.args[0])


        # SR
if __name__ == "__main__":
    app.run()


# 主動發
# with ApiClient(configuration) as api_client:
#     line_bot_api = MessagingApi(api_client)
#     line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token="17e1abde38ab4f8f8894eefd325fb3a4",
#                 messages=[TextMessage(text="AA")]
#             )
#         )

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
