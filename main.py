import os
import sys
from googletrans import Translator
from random import randint
import json
import tweepy
import requests
from urllib import request
from argparse import ArgumentParser
from requests_oauthlib import OAuth1Session

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

# TwitterのAPI
Twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN", None)
Twitter_access_secret = os.getenv("TWITTER_ACCESS_SECRET", None)
Twitter_API_key = os.getenv("TWITTER_API_KEY", None)
Twitter_API_secret = os.getenv("TWITTER_API_SECRET", None)
AT = os.getenv("AT")
AS = os.getenv("AS")
CS = os.getenv("CS")
CK = os.getenv("CK")

# TwitterAPIの初期設定
auth = tweepy.OAuthHandler(Twitter_API_key, Twitter_API_secret)
auth.set_access_token(Twitter_access_token, Twitter_access_secret)
sess = OAuth1Session(CK,CS,AT,AS)

TL = "https://api.twitter.com/1.1/statuses/user_timeline.json"

api = tweepy.API(auth)


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
    text =  event.message.text

    # コマンド開始位置を確認
    if text[:1] == "!":
        res_result = Track(text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))
    elif text[:1] == "?":
        res_result = Neta(text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))
    elif text[:1] == "|":
        res_result = loop(text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))
    elif text[:1] == "/":
        res_result = get_tweet(text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))
    elif text[:1] == "r":
        res_result = ran(text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))
    elif text[:1] == "+":
        res_result = add_user(text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))
    elif text[:1] == "_":
        res_result = show_user()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res_result))


    # それ以外(ただの会話とか)ならスルー
    else:
        pass

def show_user():
    a = ""
    user_dict = json.dumps("json/user.json")
    for i in user_dict:
        a += f"{i} {user_dict[i]}\n"

# trackする
def Track(text):
    # 受信したテキストを空白でリスト化
    text = text.split()

    platform_dict = json.loads("json/pf.json")
    try:
        # プラットフォームのショートカット機能
        platform = text[1]
        platform = platform_dict[platform]

        # ユーザーショートカットの実装
        user = text[2]
        user_dict = json.loads("json/user.json")
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
    resa = res["data"]["segments"][0]["stats"]
    # コマンドごとにdictから検索

    res_dict = {
        "rank":resa["rankScore"]["metadata"]["rankName"],
        "rankscore":resa["rankScore"]["displayValue"],
        "id":res["data"]["platformInfo"]["platformUserId"],
        "level":resa["level"]["displayValue"],
        "arena":resa["arenaRankScore"]["metadata"]["rankName"],
        "arenarank":resa["arenaRankScore"]["displayValue"],
        "kill":resa["kills"]["displayValue"]
    }
 
    if what in res_dict:
        res_result = res_dict[what]
    else:
        res_result = "そんなコマンドないけど？w"
    return res_result

def add_user(text):
    text = text.split()
    try:
        username = text[1]
        shortcut = text[2]
    except:
        return "ばか！！！！！！！！！"

    user_dict = json.loads("json/user.json")
    user_dict[shortcut] = username
    with open("json/user.json","w") as f:
        json.dump(user_dict,f,indent=4)
    
    return "ショートカットを追加しましたやったね"

def loop(text):
    text = text.split()
    what = text[1]
    try:
        leng = int(text[2])
        wtf = what*leng
        if len(wtf) > 500:
            wtf = wtf[:500]
    except:
        wtf = "ばかは宿題やって寝ろ"
    
    return wtf
 
def Neta(text):
    text = text.split()
    what = text[1]

    neta_dict = json.loads("json/neta.json")
    
    if what in neta_dict:
        res_result = neta_dict[what]
    else:
        res_result = "そんなコマンドないってw"
    return res_result

def get_tweet(text):
    tweet = ""
    text = text.split()
    userID = text[1]
    try:
        count = int(text[2])
    except:
        count = 1

    if count > 10:
        count = 10
        
    user_dict = {
            "h":"hayaa6211",
            "i":"ITia_AISIA",
            "k":"kaijyuukun2001",
            "a":"amazonesu_iwata",
            "sh":"KNR_ShibuyaHal",
            "e":"eerie0w0eery",
            "m":"iMarshi FB",
            "kh":"_kuroki_Honoka",
        }

    if userID in user_dict:
        userID = user_dict[userID]
    else:
        pass

    param = {
        "screen_name":userID,
        "count":count,
        "include_entities" : True,
        "exclude_replies" : True,
        "include_rts" : True
    }
    try:
        req = sess.get(TL, params=param)
        timeline = json.loads(req.text)
        t = "-"*20
        for twee in reversed(timeline):
            tweet += twee["text"] + "\n" + t + "\n"
        tt = f"{userID}さんの最新ツイート{count}件です\n{t}\n{tweet}"
    except:
        tt = f"{userID}は見つかりませんでした．"
    return tt

def ran(text):
    try:
        text = text.split()
        try:
            n = int(text[1])
        except:
            n = 1
        try:
            m = int(text[2])
        except:
            n = 1
            m = int(text[1])
    except:
        ans = "引数を指定しやがれください"
    try:
        count = int(text[1])
        ans = randint(n,m)
    except:
        ans = "数字を指定しやがれください"
    return ans


#変えるな
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)