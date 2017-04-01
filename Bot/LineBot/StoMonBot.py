import sys,requests,json,time,sys,datetime
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from util.AppUtil import AppUtil

app = Flask(__name__)
appUtil = AppUtil()
STOCK_MIS = appUtil.getStockMIS()
RT_URL = appUtil.getStockRealTimePrice()
stockIDList = appUtil.getStockIDs().split(',')

# get channel_secret and channel_access_token from your environment variable
channel_secret = appUtil.getLineChannelSecret()
channel_access_token = appUtil.getLineChannelAccessToken()
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    print('got callback')
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'
 
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    defRtnStr = 'Don\'t call me , I will call you.'


    reciveMsg = event.message.text

    print('YYYYYYYYYYYYYYYY')
    print(event.reply_token)
    print(event.message.text)
    print('xxxxxxxxxx')

    matching = [s for s in stockIDList if reciveMsg in s]
    if (len(matching) == 0):
       defRtnStr = 'Don\'t have this stockId.' 
    else:
        with requests.session() as req:
            req.get(STOCK_MIS,
                        headers={'Accept-Language': 'zh-TW'})

            timestamp = int(time.time()*1000+1000000)
            print(RT_URL.format(timestamp,matching[0]))
            res = req.get(RT_URL.format(timestamp,matching[0]))
            jsonRtn = res.text.strip()
            d = json.loads(jsonRtn)
            datas = d['msgArray']
            df = pd.DataFrame(columns=['c','n','z','t','tv'])
            for data in datas :
                try:
                    data = dict((key,data[key]) for key in ('c','n','z','t','tv'))
                    df = df.append(data,ignore_index=True)
                except Exception as e:
                    print('something is null.')
            print(df)
            defRtnStr = str(df.loc[0,'c']) + ' ' + str(df.loc[0,'n']) + ' ' + str(df.loc[0,'z']) + ' ' + str(df.loc[0,'t']) + ' ' + str(df.loc[0,'tv'])

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=defRtnStr))

@app.route('/')
def index():
    return "<p>Hello StoMonBot!</p>"
    
if __name__ == '__main__':
    app.run(debug=True)