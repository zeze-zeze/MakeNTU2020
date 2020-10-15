from flask import Flask, request, abort
from __main__ import APP, waiting_queue

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('XXXXXXXXXX')
handler = WebhookHandler('XXXXXXXXXX')

@APP.route("/test", methods=['GET'])
def test():
    reply = ''
    a = 1
    for wq in waiting_queue:
        if a != wq['id']:
            reply += str(wq['id'])
    return reply

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
        res = int(event.message.text)
        for wq in waiting_queue:
            if res == wq['id']:
                reply = 'Waiting Time: about {} minutes '.format(wq['wait'])
                break
            else:
                reply = 'No such number !'

    except:
        reply = 'Usage: Input the number, and you will get the time to wait'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

