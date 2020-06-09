# CloudRun 用にコード変更する

## 追加したもの

+ Dockerfile
  + CloudRun でも同様に必要
+ docker-build-run.sh
  + ローカルでテストするためのもの
  + 必要が無くなれば、削除する

## 変更点

main.py

+ 起動 アドレス を変更
  + 127.0.0.1 -> 0.0.0.0


## 実行方法

+ GCP との認証

```
gcloud auth login
```

+ GCP のプロジェクトの設定

```
export pj_id='hogehoge'
```
```
gcloud config set project ${pj_id}
```

+ GCR にコンテナイメージをデプロイする

```
gcloud builds submit --tag gcr.io/${pj_id}/gcp-line-bots
```

+ Cloud Run をデプロイする
  + 実際は GCR にデプロイしたコンテナイメージを指定して実行しているだけ

```
gcloud run deploy \
  --image gcr.io/${pj_id}/gcp-line-bots \
  --platform managed \
  --region asia-northeast1
```


## 以下めも

+ シークレットは 環境変数は非推奨で、シークレットマネージャを使うのが推奨
  + https://cloud.google.com/run/docs/configuring/environment-variables
  + 今回は以下の変数が必要になる
    + user_id
    + channel_secret
    + channel_access_token
    + URL(たぶんCloudRun)