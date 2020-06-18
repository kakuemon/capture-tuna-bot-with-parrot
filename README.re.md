# CloudRun 用にコード変更する

## 追加したもの

+ Dockerfile
  + CloudRun でも同様に必要
+ docker-build-run.sh
  + ローカルでテストするためのもの
  + 必要が無くなれば、削除する

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

+ GCS のバケットを作成

```
gsutil mb gs://${pj_id}-gcp-line-bots-01
gsutil ls | grep ${pj_id}-gcp-line-bots-01

---> 出来ていればOK
```

+ GCS にイメージのアップロード

```
gsutil cp static/images/*.png gs://${pj_id}-gcp-line-bots-01/
gsutil ls gs://${pj_id}-gcp-line-bots-01

---> 出来ていればOK
```

+ GCS にアップロードしたイメージを一般公開する

```
gsutil iam ch allUsers:objectViewer gs://${pj_id}-gcp-line-bots-01
```



+ 設定ファイルをコピーして項目を埋める

```
cp -a app.yaml.sample app.yaml
```
```
vim app.yaml
```


+ GAE にデプロイ

```
gcloud app deploy
```

+ LINE Developer に GAE の URL を登録する

IMG

## 実行方法 Cloud Run

+ 公式ドキュメント
  + https://cloud.google.com/run/docs/quickstarts/build-and-deploy#python
  + https://cloud.google.com/run/docs/configuring/environment-variables#yaml

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

+ Dockerfile の作成

```
cp -a Dockerfile.sample Dockerfile
```

+ 修正

```
vim Dockerfile
```





+ GCR にコンテナイメージをデプロイする

```
gcloud builds submit --tag gcr.io/${pj_id}/gcp-line-bots
```


+ Cloud Run をデプロイする
  + 実際は GCR にデプロイしたコンテナイメージを指定して実行しているだけ
  + `--allow-unauthenticated` をつけることで公開を許容
  + https://cloud.google.com/run/docs/authenticating/public?hl=en#gcloud

```
gcloud run deploy gcp-line-bots \
  --image gcr.io/${pj_id}/gcp-line-bots \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated
```
```
### 出力例

$ gcloud run deploy \
>   --image gcr.io/${pj_id}/gcp-line-bots \
>   --platform managed \
>   --region asia-northeast1
Service name (gcp-line-bots):  
Deploying container to Cloud Run service [gcp-line-bots] in project [your GCP project ID] region [asia-northeast1]
✓ Deploying... Done.                                                                                                                                                                   
  ✓ Creating Revision...                                                                                                                                                               
  ✓ Routing traffic...                                                                                                                                                                 
Done.                                                                                                                                                                                  
Service [gcp-line-bots] revision [gcp-line-bots-00003-gej] has been deployed and is serving 100 percent of traffic at https://gcp-line-bots-3umtulj4sq-an.a.run.app

```


## 以下めも

+ シークレットは 環境変数は非推奨で、シークレットマネージャを使うのが推奨
  + https://cloud.google.com/run/docs/configuring/environment-variables
  + 今回は以下の変数が必要になる
    + user_id(<- どこで使っているか分からないので、チェックが必要)
    + channel_secret
    + channel_access_token
    + GCS のバケット名
