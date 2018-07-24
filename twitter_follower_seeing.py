import json
from requests_oauthlib import OAuth1Session
import time

CK = "9hHpHgwHErwwDNkN2vrUtfPek"
CS = "TiuYZh9xqzHYFeHxmGffgWnAFMWZtBvvYSftCHgpRgB7M67sJL"
AT = "133292143-9TTJxuj4HcfSkMkZlHy0Sz3gbd0XGcEiBGkMi1jc"
ATS = "IQ0ksP6UX7zgM5H2ejxt8lytDnTIs80zhX1VR6Baaxm6z"

twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params ={'count' : 5}
res = twitter.get(url, params = params)

"""
if res.status_code == 200: #正常通信出来た場合
    timelines = json.loads(res.text) #レスポンスからタイムラインリストを取得
    for line in timelines: #タイムラインリストをループ処理
        print(line['user']['name']+'::'+line['text'])
        print(line['created_at'])
        print('*******************************************')
else: #正常通信出来なかった場合
    print("Failed: %d" % res.status_code)
"""
while True:
    time.sleep(1)
    cursor = -1
    while cursor != 0:
        # 情報取得
        api = 'https://api.twitter.com/1.1/followers/list.json'
        params = {'screen_name':"KUNImt_Sun", 'cursor':cursor, 'count':'200', 'skip_status':'true', 'include_user_entities':'false'}
        res = twitter.get(api, params = params)

        # 辞書変換
        dic = json.loads(res.text)

        # 出力
        users = dic['users']
        temp_list =[]
        for user in users:
            temp_list.append(user['screen_name'])
        cursor = dic['next_cursor']
    print(temp_list, len(temp_list))
