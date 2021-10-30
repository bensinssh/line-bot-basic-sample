import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('2CNmJsIBAOJ1g/UbGV/NquzQitvnT+/RV+hkJmdJdt3S5pXfgF1lZrLnqNUL17fT3/scIGdWNmeH1P0mpIhFDTuy54MPJARb7FPKVOqy4x1KPLfS5jDwnOg7FPKVOqy4x1KPLfS5jDwnOg4x2'​)
handler = WebhookHandler('e34f51f308839a2ff250c2c49c6c9046')


@app.route('/')
def index():
    return 'You call index()'


@app.route('/push_sample')
def push_sample():
    """プッシュメッセージを送る"""
    user_id = ('Uc61951ca6874dac8f0ec611c59923489')​
    line_bot_api.push_message(user_id, TextSendMessage(text='Hello World!'))

    return 'OK'


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=event.message.text))


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
