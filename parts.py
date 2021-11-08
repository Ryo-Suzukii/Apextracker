import os
import json
import requests

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
#----------------------

class Main:
    
    def track(self,pf,usr,cmd):
        self.pf = pf
        self.usr = usr
        self.cmd = cmd
        url = "https://public-api.tracker.gg/v2/apex/standard/profile"

        with open("json/pf.json",mode="r") as f:
            pf_dict = json.load(f)
        self.pf = pf_dict[self.pf]

        with open("json/user.json",mode="r") as f:
            usr_dict = json.load(f)
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
        
        return res_result