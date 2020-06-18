from flask import Flask, request
import random, json, requests
import pandas as pd



# line用ライブラリ
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,ImageSendMessage
)

import os
# conunt maguro 
maguro_count=0

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET       = os.environ["YOUR_CHANNEL_SECRET"]
STORAGE_BUCKET            = os.environ["STORAGE_BUCKET"]

# random choice


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# LINE APIおよびWebhookの接続s
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler      = WebhookHandler(YOUR_CHANNEL_SECRET)

def maguro_image_message():
    messages = ImageSendMessage(
        original_content_url = STORAGE_BUCKET + "/maguro.png", #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url    = STORAGE_BUCKET + "/maguro_mini.png" #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    )
    return messages

def neta_image_message():
    messages = ImageSendMessage(
        original_content_url = STORAGE_BUCKET + "/sushi.png", #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url    = STORAGE_BUCKET + "/sushi.png" #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    )
    return messages

# Flaskのルート設定
@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# メッセージ応答メソッド
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #　メッセージは "event.message.text" という変数に格納される
    if event.message.text == "おはよう":
        text = "おはようございます"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif event.message.text == "スタンプ":
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(package_id=1 ,sticker_id=1)
        )
    elif event.message.text == "マグロ":
        messages = maguro_image_message()
        line_bot_api.reply_message(
            event.reply_token,
            messages
            )

    elif event.message.text == "捕獲":
        global maguro_count
        messages = random.choice(["捕獲成功","逃げられた","残念"])
        if messages == "捕獲成功":
            maguro_count += 1
            messages1 = "現在マグロは" + str(maguro_count) + "匹"
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=messages),TextSendMessage(text=messages1)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text=messages)
            )

    elif event.message.text == "逃がす":
        global maguro_count
        maguro_count = 0
        messages = "マグロは逃げた"
        messages = maguro_image_message()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=messages) 
        )

    elif event.message.text == "マグロ一丁":
        global maguro_count
        if maguro_count > 2:
            messages = "へい、おまち！"
            maguro_count = 0
            neta_message = neta_image_message()
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text=messages),neta_message]
                )
        else:
            messages = "マグロとってきて！"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=messages)
                )


    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080))
    )
# [END gae_python37_app]
