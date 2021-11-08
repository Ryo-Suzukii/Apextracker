import os
import sys
import json
import tweepy
from random import randint
import requests
from requests_oauthlib import OAuth1Session

#-----API KEY-----------
Tracker_api = "94a1b88a-7bdb-43cb-a3d6-b633a0aa8f47"
Twitter_access_token = "877115268631113729-ZQieIvXNgMG9pqkUb1rRkBoJ7lVXZvm"
Twitter_access_secret = "HT0HGwnKrhHSyPGDcK8E0duqxukjnMIX0DKYZqWAPZmFZ"
Twitter_API_key = "Lv5GImN3GnuIjD9sijvdMMCrv"
Twitter_API_secret = "j1Ug6CYaU29hsFMT5OgTNiBlACxmHXZETjFQQ4J9Xrbl87PG1o"
AT = "877115268631113729-ZQieIvXNgMG9pqkUb1rRkBoJ7lVXZvm"
AS = "HT0HGwnKrhHSyPGDcK8E0duqxukjnMIX0DKYZqWAPZmFZ"
CS = "j1Ug6CYaU29hsFMT5OgTNiBlACxmHXZETjFQQ4J9Xrbl87PG1o"
CK = "Lv5GImN3GnuIjD9sijvdMMCrv"

auth = tweepy.OAuthHandler(Twitter_API_key, Twitter_API_secret)
auth.set_access_token(Twitter_access_token, Twitter_access_secret)
sess = OAuth1Session(CK,CS,AT,AS)
api = tweepy.API(auth)

TL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
#----------------------

ERROR_MESSAGE = "An error occurred during program execution. Please ask the administrator for details."

class Main:
    
    def track(self,pf,usr,cmd):
        try:
            self.pf = pf
            self.usr = usr
            self.cmd = cmd
            url = "https://public-api.tracker.gg/v2/apex/standard/profile"

            with open("json/pf.json",mode="r") as f:
                pf_dict = json.load(f)
            if self.pf in pf_dict:
                self.pf = pf_dict[self.pf]

            with open("json/user.json",mode="r") as f:
                usr_dict = json.load(f)
            if self.usr in usr_dict:
                self.usr = usr_dict[self.usr]
            

            url = f"{url}/{self.pf}/{self.usr}"

            res = requests.get(url,headers={"TRN-Api-Key":Tracker_api}).json()
            resa = res["data"]["segments"][0]["stats"]

            res_dict = {
            "rank":resa["rankScore"]["metadata"]["rankName"],
            "rankscore":resa["rankScore"]["displayValue"],
            "id":res["data"]["platformInfo"]["platformUserId"],
            "level":resa["level"]["displayValue"],
            "arena":resa["arenaRankScore"]["metadata"]["rankName"],
            "arenarank":resa["arenaRankScore"]["displayValue"],
            "kill":resa["kills"]["displayValue"]
            }

            if self.cmd in res_dict:
                res_result = res_dict[self.cmd]
            else:
                res_result = "コマンドが存在しないよばか"
            
            return f"{self.usr}さんの{self.cmd}は{res_result}です"
        except:
            return ERROR_MESSAGE
    
    def loop(self,txt,length):
        try:
            self.txt = txt
            self.length = int(length)

            try:
                res = txt*length
                res = res[:200]
            except:
                res = "バカは宿題やって寝ろ"
            
            return res
        except:
            return ERROR_MESSAGE+"/"+sys._getframe().f_code.co_name
    
    def neta(self,txt):
        try:
            with open("json/neta.json",mode="r",encoding="utf-8") as f:
                neta_dict = json.load(f)
            
            if txt in neta_dict:
                res = neta_dict[txt]
            else:
                res = "そんなコマンドないが?w"
            
            return res
        except:
            return ERROR_MESSAGE+"/"+sys._getframe().f_code.co_name
    
    def get_tweet(self,user,count):
        tweet = ""
        try:
            self.user = user
            self.count = count

            if self.count > 10:
                self.count = 10
            
            with open("json/user.json",mode="r") as f:
                user_dict = json.load(f)
            
            if self.user in user_dict:
                self.user = user_dict[self.user]
            else:
                pass

            param = {
            "screen_name":self.user,
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
                tt = f"{self.user}さんの最新ツイート{count}件です\n{t}\n{tweet}"
            except:
                tt = f"{self.user}は見つかりませんでした．"

            return tt
        except:
            return ERROR_MESSAGE+"/"+sys._getframe().f_code.co_name
    
    def random(self,start,end,mode=0):
        self.start = int(start)
        self.end = int(end)
        self.mode = mode

        try:
            ans = randint(start,end)

            return ans

        except:
            return ERROR_MESSAGE+"/"+sys._getframe().f_code.co_name

class to_dict:
    def __init__(self):
        pass

    def add_user(self,sc,m):
        try:
            with open("json/user.json",mode="r") as f:
                user_dict = json.load(f)
            user_dict[sc] = m

            with open("json/user.json",mode="w",encoding="utf-8") as f:
                json.dump(user_dict,f,indent=4)
        except:
            return "user情報を辞書に追加できませんでした．時間をおいて再度実行してください．"
        
        return f"{sc}を{m}として辞書に追加しました．"

    def del_dict(self,sc):
        try:
            with open("json/user.json",mode="r") as f:
                user_dict = json.load(f)
            
            try:
                del user_dict[sc]
            except:
                return f"辞書の中に{sc}はありません"
            
            with open("json/user.json",mode="w",encoding="utf-8") as f:
                json.dump(user_dict,f,indent=4)
        except:
            return "user情報を削除できませんでした．時間をおいて再度実行してください．"
    
    def view_dict(self):
        try:
            with open("json/user.json",mode="r") as f:
                user_dict = json.load(f)
            a = ""
            for n in user_dict:
                a += f"{n}:{user_dict[n]}\n"

        except:
            return "なんでか知らんけど辞書の中身見れないや"
        
        return a
