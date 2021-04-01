import os
import sys
import json
import requests
from argparse import ArgumentParser

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

app = Flask(__name__)

# LINEのAPIキーを環境変数からもってくる
Tracker_api = os.getenv('Tracker_API',None)
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


url = "https://public-api.tracker.gg/v2/apex/standard/profile"
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
head = {"TRN-Api-Key":Tracker_api}


@app.route("/callback", methods=['POST'])
# 触るな
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
        abort(400)

    return 'OK'


#メッセージ受け取ったとき
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # コマンド開始位置を確認
    if event.message.text[:1] == "!":
        res_result = Track(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))
    elif event.message.text[:1] == "?":
        res_result = Neta(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))
    elif event.message.text[:1] == "|":
        res_result = loop(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))

    # それ以外(ただの会話とか)ならスルー
    else:
        pass

# trackする
def Track(text):
    # 受信したテキストを空白でリスト化
    text = text.split()

    platform_dict = {
        "p":"psn",
        "o":"origin",
        "psn":"psn",
        "origin":"origin",
        "x":"xbl",
        "xbox":"xbl"
    }
    try:
        # プラットフォームのショートカット機能
        platform = text[1]
        platform = platform_dict[platform]

        # ユーザーショートカットの実装
        user = text[2]
        user_dict = {
            "h":"hayaa6211",
            "i":"ITia_AISIA",
            "k":"kaijyuukun2001",
            "a":"amazonesu_iwata",
            "sh":"KNR_ShibuyaHal",
            "e":"eerie0w0eery",
            "m":"iMarshi FB"
        }
        if user in user_dict:
            user = user_dict[user]

        # コマンド内容
        what = text[3]
    except:
        return "そのコマンドおかしいで(platform)"

    # ユーザーごとのurlを作成して検索
    user_url = f"{url}/{platform}/{user}"
    #jsonで検索結果まとめる
    res = requests.get(user_url, headers=head).json()

    # コマンドごとにdictから検索
    if what == "rank":
        res_result = res["data"]["segments"][0]["stats"]["rankScore"]["metadata"]["rankName"]
    elif what == "rankscore":
        res_result = res["data"]["segments"][0]["stats"]["rankScore"]["displayValue"]
    elif what == "id":
        res_result = res["data"]["platformInfo"]["platformUserId"]
    elif what == "level":
        res_result = res["data"]["segments"][0]["stats"]["level"]["displayValue"]
    elif what == "kill":
        res_result = res["data"]["segments"][0]["stats"]["kills"]["displayValue"]
    elif what == "s5w":
        res_result = res["data"]["segments"][0]["stats"]["season5Wins"]["displayValue"]
    elif what == "s5k":
        res_result = res["data"]["segments"][0]["stats"]["season5Kills"]["displayValue"]
    elif what == "s6w":
        res_result = res["data"]["segments"][0]["stats"]["season6Wins"]["displayValue"]
    elif what == "s6k":
        res_result = res["data"]["segments"][0]["stats"]["season6Kills"]["displayValue"]
    elif what == "s7w":
        res_result = res["data"]["segments"][0]["stats"]["season7Wins"]["displayValue"]
    elif what == "s7k":
        res_result = res["data"]["segments"][0]["stats"]["season7Kills"]["displayValue"]
    elif what == "s8w":
        res_result = res["data"]["segments"][0]["stats"]["season8Wins"]["displayValue"]
    elif what == "s8k":
        res_result = res["data"]["segments"][0]["stats"]["season8Kills"]["displayValue"]
    else:
        res_result = "そんなコマンドないんだよね"
    return res_result

def loop(text):
    text = text.split()
    what = text[1]
    wtf = what*100
    if len(wtf) > 500:
        wtf = wtf[:500]
    return wtf
 
def Neta(text):
    text = text.split()
    what = text[1]

    neta_dict = {
        "help":"! [platform(psn or origin or xbl)] [playerName] [コマンド] です．\nコマンドは現在[rank],[rankscore],[id],[level],[kill],[s[n]k or w]です",
        "fuck":"ごめんね by黒木ほの香",
        "ramen":"https://tabelog.com/tokyo/A1303/A130301/13069220/",
        "home":"https://nit-komaba.ed.jp/",
        "version":"v1.2.1(release 2021/04/01)",
        "黒木ほの香":"https://twitter.com/_kuroki_honoka",
        "青木志貴":"https://twitter.com/eerieXeery",
        "えなこ":"https://twitter.com/enako_cos",
        ":)":"なにわろてんねん",
        ":(":"元気出して",
        "playlist":"https://www.youtube.com/playlist?list=PLSlDAq60dYFASz84xcS2sXwjf34maoIGR"
    }
    
    if what in neta_dict:
        res_result = neta_dict[what]
    else:
        res_result = "そんなコマンドないってw"
    return res_result


#変えるな
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)