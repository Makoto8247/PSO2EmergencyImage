import json,config
from requests_oauthlib import OAuth1Session,OAuth1
import requests
import urllib.request
import os
import PSO2EI as ei
import datetime as dt
import concurrent.futures
import pickle
import signal
import time
signal.signal(signal.SIGINT, signal.SIG_DFL)

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

schedule_id = "Washi_Schedule"

url_text = "https://api.twitter.com/1.1/statuses/update.json" 
url_media = "https://upload.twitter.com/1.1/media/upload.json"

def __init__():
    ei.Make_Schedule()

def Bal_Day():
    now_day = dt.date.today().day
    bal_day = []
    bal = False
    id_list_pass = os.path.abspath("./bal_day.pkl")
    if os.path.isfile(id_list_pass):
        with open(id_list_pass,mode='rb') as f:
            bal_day = pickle.load(f)
        for i in bal_day:
            if now_day == i:
                bal = True
                break
    return bal


def rep(tweet_id,user_name):
    if user_name != schedule_id:
        img_url = os.path.abspath("./day.png")
        message = "@" + user_name + "\nリプライありがとうございます。\n本日の緊急の予定はこちらです。"
        if Bal_Day():
            message += "\n本日はバルロドスのデイリーがあります。"
        files = {"media" : open(img_url,"rb")}
        req_media = twitter.post(url_media, files = files)
        # レスポンス
        if req_media.status_code != 200:
            print ("画像アップロード失敗: %s", req_media.text)
            exit()

        # media_id を取得
        media_id = json.loads(req_media.text)['media_id']
        params = {'status': message, 'in_reply_to_status_id':tweet_id ,'media_ids': [media_id]}
        req_media = twitter.post(url_text, params = params)

def rep_search():
    try:
        id_list_pass = os.path.abspath("./id_list.pkl")
        while True:
            old_tweets = {}
            # リスト呼び出し
            if os.path.isfile(id_list_pass):
                with open(id_list_pass,mode='rb') as f:
                    old_tweets = pickle.load(f)
            time.sleep(0.5)
            cnt_range = 50
            tweets = {}
            user_id = "@Washi_Schedule exclude:retweets"
            url = "https://api.twitter.com/1.1/search/tweets.json"
            auth = OAuth1(CK,CS,AT,ATS)
            params = {'q':user_id,'count':cnt_range}
            response = requests.get(url, auth=auth,params=params)
            data = response.json()['statuses']
            for tweet in data:
                id_int = tweet['id']
                user = tweet['user']['screen_name']
                tweets[id_int] = user
            # 重複確認
            time.sleep(1)
            for tweet_id,tweet_user_id in tweets.items():
                flg = True
                if len(old_tweets) != 0:
                    for old_tweet_id in old_tweets:
                        if tweet_id == old_tweet_id:
                            flg = False
                            break
                if flg:
                    # リプライ送信
                    rep(tweet_id,tweet_user_id)
            time.sleep(1)
            if len(tweets) > 0:
                # リスト保存
                with open(id_list_pass,mode='wb') as f:
                    pickle.dump(tweets,f)
                time.sleep(0.5)

    except KeyboardInterrupt:
        pass
    finally:
        pass


def syu_twi():
    img_url = os.path.abspath("./emergency.png")
    files = {"media" : open(img_url,"rb")}
    req_media = twitter.post(url_media, files = files)
    # レスポンス
    if req_media.status_code != 200:
        print ("画像アップロード失敗: %s", req_media.text)
        exit()

    # media_id を取得
    media_id = json.loads(req_media.text)['media_id']

    # 投稿した画像をツイートに添付したい場合はこんな風に取得したmedia_idを"media_ids"で指定してツイートを投稿
    message = '今週の緊急クエストはこちらです\n' + '#PSO2 #緊急クエスト'
    params = {'status': message, "media_ids": [media_id]}
    req_media = twitter.post(url_text, params = params)

def main():
    try:
        old_weekday = dt.date.today().weekday()
        while True:
            weekday = dt.date.today().weekday()
            now_time = dt.datetime.now()
            if weekday == 2 and now_time.hour == 20 and now_time.minute == 0 and now_time.second == 30: # 水曜日の時
                ei.Make_Schedule()
                syu_twi()
            if weekday != old_weekday:
                ei.Make_Schedule()
                old_weekday = weekday
    except KeyboardInterrupt:
        pass
    finally:
        pass
        

if __name__ == "__main__":
    try:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        executor.submit(main)
        executor.submit(rep_search)
    except KeyboardInterrupt:
        pass
    finally:
        pass
