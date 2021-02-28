from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
import requests
import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊

@app.route("/callback",methods=['POST',"GET"])
def callback():
    if request.method == 'GET':
        print("receive get request")
        with open('id.txt', 'r') as f:
            user_id = f.read()
        f.close()
        print(user_id)
        try:
            line_bot_api.broadcast(TextSendMessage(text='This is a broadcast message'))
            line_bot_api.push_message(user_id, TextSendMessage(text='Message from Desktop send to specific id'))
            line_bot_api.push_message(user_id,ImageSendMessage(original_content_url="https://i.imgur.com/PQ6Y1vv.png#",
                                                               preview_image_url="https://i.imgur.com/PQ6Y1vv.png#"))
        except LineBotApiError as e:
            # error handle
            raise e
        return "OK"
        pass
    elif request.method == 'POST':
        signature = request.headers['X-Line-Signature']

        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        try:
            print(body, signature)
            handler.handle(body, signature)

        except InvalidSignatureError:
            abort(400)

        return 'OK'


# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    if event.message.text == "setreply":
        var_id = (event.source.user_id)
        with open('id.txt', 'w') as f:
            f.write(str(var_id))
            f.close()
    elif (event.message.text == "photo"):
        pass
        data = {
            "name": "Jason",
            "photo": "ON"
        }
        print(data.keys())
        # "message from desktop"
        r = requests.get('https://aaf0b0213f31.ngrok.io', params=data)
        r.close()
    elif (event.message.text == "hi"):
        pass
        data = {
            "name": "Jason",
            "photo": "OFF"
        }
        # print(data.keys())
        # "message from desktop"
        r = requests.get('https://aaf0b0213f31.ngrok.io/hi', params=data)
        r.close()
    else:
        pass

# @handler.add(MessageEvent, message=TextMessage)
# def pretty_echo(event):
#     # if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
#
#     # Phoebe 愛唱歌
#     pretty_note = '♫♪♬'
#     pretty_text = ''
#
#     for i in event.message.text:
#         pretty_text += i
#         pretty_text += random.choice(pretty_note)
#
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=pretty_text)
#     )
if __name__ == "__main__":
    app.run()