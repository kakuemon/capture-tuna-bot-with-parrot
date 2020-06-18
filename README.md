# マグロ LINE-BOTをGCPで使う方法

#  1. 事前準備

## LINE Developerのアカウント作成

[LINE Developers](https://developers.line.biz/ja/)にログインしてMessaging APIのチャネルを作成する。

チャネルの作り方は[公式ドキュメント](https://developers.line.biz/ja/docs/messaging-api/getting-started/#%E3%83%81%E3%83%A3%E3%83%8D%E3%83%AB%E3%81%AE%E4%BD%9C%E6%88%90)を参照

作成したチャネル内にある`user_id`, `channel_secret` および `channel_access_token`をメモしてapp.yamlに入力する。

 ~~~yaml
env_variables:
  USER_ID: "***"
  YOUR_CHANNEL_SECRET: "***"
  YOUR_CHANNEL_ACCESS_TOKEN: "***"
~~~

## GCP(Google Cloud Platform)登録

[Google Cloud Platform](https://cloud.google.com/getting-started?hl=ja)に登録する。クレジットが必要。新規の場合は $300 相当の無料クレジットがつく。

[コチラ](https://blog.apar.jp/web/6912/)を参考に新しいプロジェクトを作成し、Google Apps Engineを`Python`言語で設定する。GCPではwebにてターミナル環境を提供しているため、そちらを利用する。

gcloudコマンドが使用可能になっていることを確認する。
~~~
$ gcloud -v
Google Cloud SDK 293.0.0
bq 2.0.57
core 2020.05.15
gsutil 4.50
~~~

Google Apps Engineのサービスからでdefaultをクリックし現在のURLをメモする。


## マグロの画像準備

デフォルトではイラストやの画像があるので、初期設定のままでいい場合は設定不要。画像を変更したい場合は、static/images/に使用したいマグロ画像の準備を行う。なおLINEではプレビュー用とオリジナル用で2枚必要になる。

# 2. 使い方

## GCPへデプロイ

ダウンロードしてきたソースコードを一度デプロイしてURLを取得する。このときデプロイ先のプロジェクトがあっているか確認する。

~~~
$ cd your/download/path...
$ gcloud app deploy

Services to deploy:

descriptor:      [***]
source:          [***]
target project:  [linebot-20200604-first]
target service:  [default]
target version:  [20200606t085713]
target url:      [***]


Do you want to continue (Y/n)? Y 


Beginning deployment of service [default]...
╔════════════════════════════════════════════════════════════╗
╠═ Uploading 4 files to Google Cloud Storage                ═╣
╚════════════════════════════════════════════════════════════╝
File upload done.
Updating service [default]...done.
Setting traffic split for service [default]...done.
Deployed service [default] to [***]

You can stream logs from the command line by running:
  $ gcloud app logs tail -s default

To view your application in the web browser run:
  $ gcloud app browse

Updates are available for some Cloud SDK components.  To install them,
please run:
  $ gcloud components update

~~~

ここでデプロイが完了したら、先ほどメモしたURLを開くと、hello worldが確認できる

LINE Developerを開きMessaging API内のwebhook URLに設定する。このときにURLの後ろに/callbackをつけるようにする

`{コピーしたURL}/callback`

<img width="1028" alt="スクリーンショット 2020-06-06 9 07 22" src="https://user-images.githubusercontent.com/55194591/83931484-f47f1d80-a7d7-11ea-86e9-f231b6c53511.png">

またmain.pyを下記のように編集する。

~~~~python
def maguro_image_message():
    messages = ImageSendMessage(
        original_content_url="{コピーしたURL}/images/maguro.png", 
        preview_image_url="{コピーしたURL}/images/maguro_mini.png" 
    )
    return messages

def neta_image_message():
    messages = ImageSendMessage(
        original_content_url="{コピーしたURL}/images/sushi.png", 
        preview_image_url="{コピーしたURL}/images/sushi.png" 
    )
    return messages
~~~~



## 動作確認

 ### LINE botをMessaging API設定のタブのQRから追加して友達になる。何かコマンドを送るとおうむ返しされる。

 ### 「おはよう」→「おはようございます」

### 「マグロ」→ネタの画像

### 「捕獲」→まぐろ捕獲チャレンジが開始

### 「逃がす」→捕まえたマグロを逃がす

### もしエラーが発生した場合は、GCPのError Reportingを利用する。もしくはコマンドにてエラーログを確認する

~~~
$ gcloud app logs tail -s default
~~~



## LIBRARY
- line-bot-sdk:
    - PythonでLINE Messaging APIを使用するためのSDK(ソフトウェア開発キット）
    - https://pypi.org/project/line-bot-sdk/
    - https://github.com/line/line-bot-sdk-python
- flask:
    - Python用の軽量なWebアプリケーションフレームワーク
    - WebサイトやWebアプリケーションを作るための機能を提供する
    - https://pypi.org/project/Flask/
    - https://a2c.bitbucket.io/flask/
- requests:
    - PythonのHTTP通信ライブラリ
    - Webサイトの情報取得や画像の収集などを行うことができる
    - https://requests-docs-ja.readthedocs.io/en/latest/
- pandas:
    - Pythonでデータ解析を行うための機能を持ったライブラリで、数表や時系列データを操作するためのデータ構造を作ったり演算を行うことができる
    - https://pypi.org/project/pandas/
    - https://pandas.pydata.org/pandas-docs/stable/
