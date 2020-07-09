# チャットロボット
会話型ロボット

## 主な仕様
ユーザーからのインプットを待ち受けてデータを保存し、
保存した情報からAPIを活用して提案するロボット。

## バージョン
- Python 3.8.3
- Django 3.0.7

## ファイル作成1
cd django-robot/src/robot_project/robot_project && touch settings_local.py

settings_local.pyファイル内記述

- SECRET_KEY = 'ここにsecret_key'

## ファイル作成2
cd django-robot/src/robot_project/robot_project && touch .env

.envファイル内記述

- API_KEY=ここにopenweatherのAPIキー
- GNAVI_API_KEY=ここにぐるなびのAPIキー
- YOUTUBE_API_KEY=ここにopenweatherのAPIキー
- CARSENSOR_API_KEY=ここにカーセンサーのAPIキー
- NEWS_API_KEY=ここにNewsAPIのキー
- Google_API_KEY=ここにGoogleAPIのキー

APIキー取得先
- #openwathermap：https://openweathermap.org/api
- #ぐるなび：https://api.gnavi.co.jp/api/
- #Youtube：Google Cloud Platform から YouTube Data API v3を取得
- #カーセンサー：https://webservice.recruit.co.jp/doc/carsensor/
- #News: https://newsapi.org/
- #Google: Google Cloud Platformより

## 起動
- ./docom.sh build web
- ./docom.sh up -d
- docker exec -it django.web sh
- python manage.py migrate
- python manage.py createsuperuser

## 画面イメージ
<img src="https://user-images.githubusercontent.com/61681360/85812198-f9ae0780-b79a-11ea-8a1f-d44316e1b3cf.png">