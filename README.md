# WebComputingソースコード

このプログラムはSlackにインストール&権限付与済みのBotを動作させるPythonプログラムです。

Version : Python 3.8.8


---


## 使用できるSlackコマンド
1. /echo [words]
	- 続く文字列[words]をそのままBotが出力します。
	- 利用API : なし
	- 使用例(Slack上) :
		- 入力 : /echo WebComputing
		- 出力 : WebComputing
	
2. /rakuten [query]
	- 楽天Booksで[query]を入力とした検索結果をレビュー平均得点降順に一定のフォーマットで出力します。
	- 利用API : 楽天書籍検索API
	- 使用例(Slack上) :
		- 入力 : /rakuten Python
		- 出力 : 
			- 453 hits in Rakuten Books ^o^!    (keywords : "Python")
			- Display only TOP 5 books!
			- 1 : 解きながら学ぶ Pythonつみあげトレーニングブック
			- リブロワークス/株式会社ビープラウド(著) マイナビ出版(出版)  (2021年07月16日頃)
			- url -> https://books.rakuten.co.jp/rb/16755433/
			- (以下略)
	
3. /rakutenwiki [query] (未完成)
	- 検索キーワード[query]に最も類似する見出しのWikipedia記事の概要からキーフレーズを抽出し、それらを入力とした楽天Books検索結果を出力します。
	- 利用API : 楽天書籍検索API, MediaWiki API, Yahooキーフレーズ抽出(V2)API
	- 使用例(Slack上) :
		- 入力 : /rakutenwiki Python
		- 出力 : 
	
4. /now
	- 現在位置の大雑把な地名と緯度経度情報を出力します。
	- 利用API : GeoJS API
	- 使用例(Slack上) :
		- 入力 : /now
		- 出力 : I'm at Shinjuku Central Park! (35.6897, 139.6895)
		
5. /wiki [query]
	- 検索キーワード[query]に最も類似する見出しのWikipedia記事の概要とリンクを出力します。
	- 利用API :  MediaWiki API
	- 使用例(Slack上) :
		- 入力 : /wiki 新世界秩序
		- 出力 : 
			- [Search word] "新世界秩序"
			- [Summary]
			- 新世界秩序（しんせかいちつじょ、英: New World Order、略称：NWO）とは、国際政治学の用語 ~~~(中略)~~~ を指すものとしても使われる。
			- [Relevant words]
			- ジウ (小説), ハーバート・ジョージ・ウェルズ, 世界征服, 新世界より (小説), ブッシュ・ドクトリン, イルミナーティ (ガンダムシリーズ), 世界, 日本国際フォーラム, 世界政府
			- [Link] https://ja.wikipedia.org/wiki/%E6%96%B0%E4%B8%96%E7%95%8C%E7%A7%A9%E5%BA%8F
	
	
---


### 本プログラムで利用したAPI
- 楽天ブックス書籍検索API(version:2017-04-04)
	- https://webservice.rakuten.co.jp/documentation/books-book-search
- GeoJS API
	- https://www.geojs.io/
- MediaWiki APIを用いたPythonモジュール
	- https://github.com/goldsmith/Wikipedia
- Yahoo!Japan キーフレーズ抽出（V2）
	- https://developer.yahoo.co.jp/webapi/jlp/keyphrase/v2/extract.html
