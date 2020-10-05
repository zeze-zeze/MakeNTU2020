from __main__ import APP

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('6WuAKKCDLKb+CUIF7W5eRnUgBnPb9vAlzmr3R+hnwBeYvJFnbdXAmeeum0tGyXFA4EzECHX0CroKGNbV1DxYfcH/jk3Aqu0WPC8tBztnF4wIjDlrm8+/3b156rBXy+tSP3G4DqMC7YWdoyPAgGKEAwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fb0fa7acf8e727f01331ceafaca370e0')


@APP.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        req = int(event.message.text)
        for wq in waiting_queue:
            if req == wq['id']:
                reply = '等候時間大約 {} 分鐘'.format(wq['wait'])
            else:
                reply = '無此等候號碼'

    except:
        reply = '使用說明：輸入號碼牌號碼，可得知等候時間'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

