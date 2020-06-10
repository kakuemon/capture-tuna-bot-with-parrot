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


## 実行方法 Cloud Run

+ GCP との認証

```
gcloud auth login
```

+ GCP のプロジェクトの設定

```
export pj_id='your GCP project ID'
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
```
### 出力例

$ gcloud run deploy \
>   --image gcr.io/${pj_id}/gcp-line-bots \
>   --platform managed \
>   --region asia-northeast1
Service name (gcp-line-bots):  
Deploying container to Cloud Run service [gcp-line-bots] in project [ca-igarashi-test-v5v2] region [asia-northeast1]
✓ Deploying... Done.                                                                                                                                                                   
  ✓ Creating Revision...                                                                                                                                                               
  ✓ Routing traffic...                                                                                                                                                                 
Done.                                                                                                                                                                                  
Service [gcp-line-bots] revision [gcp-line-bots-00003-gej] has been deployed and is serving 100 percent of traffic at https://gcp-line-bots-3umtulj4sq-an.a.run.app

```


## 実行方法 GAE


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
gcloud config set compute/region asia-northeast1
```

+ GAE にデプロイ

```
gcloud app deploy
```


## 以下めも

+ シークレットは 環境変数は非推奨で、シークレットマネージャを使うのが推奨
  + https://cloud.google.com/run/docs/configuring/environment-variables
  + 今回は以下の変数が必要になる
    + user_id
    + channel_secret
    + channel_access_token
    + URL(たぶんCloudRun)