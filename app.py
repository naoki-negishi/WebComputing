import os
import requests
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import folium
import wikipedia
from urllib import request


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# echo words
@app.command("/echo")
def repeat_text(ack, say, command):
    ack()
    say(f"{command['text']}")

# if someone say "hello", bot ack
@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")

# search for Rakuten books with query, and output the results
@app.command("/rakuten")
def search_rakuten_books(ack, say, command):
    ack()

    url="https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    payload = {
        "applicationId": os.environ["RAKUTEN_APP_ID"], # Application ID
        "hits": 5, # max results number in a single request
        "title" : command["text"],  # search keyword
        "format" : "json",  # output form : json
        "sort" : "reviewAverage",  # sort order : review average
    }
    response = requests.get(url, params=payload)
    json_data = response.json()
    
    # concrete contents of response
    if json_data['count'] == 0:  # no hits
        say("No hits in Rakuten Books with such keywords:P")
    else:
        say(f"{json_data['count']} hits in Rakuten Books ^o^!\t(keywords : \"{command['text']}\")")
        if json_data['count'] > 5:
            say(f"Display only TOP 5 books!")

        contents = "\n".join(str(m+1)+" : "+item["Item"]["title"]+"\n\t"+item["Item"]["author"]+"(著) "+item["Item"]["publisherName"] + \
            "(出版)  ("+item["Item"]["salesDate"] + ")\n\turl -> " + item["Item"]["itemUrl"] for m, item in enumerate(json_data["Items"]))
        say(contents)

# not yet installed!
# クエリに関してWikipediaを検索し、概要からYahooキーフレーズ抽出APIでキーフレーズを抽出
# それに関連した書籍を楽天BooksAPIで検索するコマンド
@app.command("/rakutenwiki")
def repeat_text(ack, say, command):
    ack()

    # search for wikipedia
    wikipedia.set_lang("jp")
    words = wikipedia.search(command['text'])
    line = str(wikipedia.summary(words[0]))

    # extract key phrases from the abstract
    URL = "https://jlp.yahooapis.jp/KeyphraseService/V2/extract"

    def post(query):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Yahoo AppID: {}".format(os.environ["YAHOO_APP_ID"]),
        }
        param_dic = {
        "id": "1234-1",
        "jsonrpc" : "2.0",
        "method" : "jlp.keyphraseservice.extract",
        "params" : {
            "q" : query
        }
        }
        params = json.dumps(param_dic).encode()
        req = request.Request(URL, params, headers)
        with request.urlopen(req) as res:
            body = res.read()
        return body.decode()

    response = post(line)
    say(response)
    key_phrases = list(str)

    # search for Rakuten Books with the key phrases
    rakuten_books_api_url="https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"

    for key_phrase in key_phrases:
        payload = {
            "applicationId": os.environ["RAKUTEN_APP_ID"], # アプリケーションID
            "hits": 1, # 一度のリクエストで返してもらう最大個数（MAX30)
            "title" : key_phrase,  # 検索キーワード
            "format" : "json",  # 出力ファイル形式 : json
            "sort" : "reviewAverage",  # ソート順 : レビューの平均点順
        }
        response = requests.get(rakuten_books_api_url, params=payload)
        json_data = response.json()

        contents = "\n".join(str(m)+" : "+item["Item"]["title"]+"\n\t"+item["Item"]["author"]+"(著) "+item["Item"]["publisherName"] + \
            "(出版)  ("+item["Item"]["salesDate"] + ")\n\turl ---> " + item["Item"]["itemUrl"] for m, item in enumerate(json_data["Items"]))
        say(contents)

# output my current location, by using "https://www.geojs.io/"
@app.command("/now")
def locate_user(ack, say):
    ack()
    url = 'https://get.geojs.io/v1/ip/geo.json'
    data = requests.get(url).json()  # data : 'dict' type data of your current location

    # get user's concrete location via wikipedia.geoserch (using [latitude, longitude] information)
    loc = wikipedia.geosearch(data['latitude'], data['longitude'])[0]
    contents = f"I'm at {loc}! ({data['latitude']}, {data['longitude']})"
    say(contents)

    # not yet installed! <- in geojs API, order of accuracy : 10km, too bad
    # illustrate user's location on a map    
    location = [data['latitude'], data['longitude']]
    accuracy_km = data['accuracy'] * 1000
    print(accuracy_km)

    map = folium.Map(location=location, zoom_start=18)
    folium.Circle(location=location, radius= accuracy_km, color='#ff0000', fillcolor='#0000ff').add_to(map)
    map.save('temp.html')
    

# by using wikipedia API(module), get and output the most likely wikipedia page's summary for query
@app.command("/wiki")
def show_wikipedia_summary(ack, say, command):
    ack()

    wikipedia.set_lang("jp")
    words = wikipedia.search(command['text'])
    line = str(wikipedia.summary(words[0]))
    link = wikipedia.page(words[0]).url

    contents = f"[Search word] \"{words[0]}\"\n[Summary]\n{line}\n[Relevant words]\n{', '.join(words[1:])}\n[Link] {link}"
    say(contents)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()