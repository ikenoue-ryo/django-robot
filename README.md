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
- Rakuten_API_KEY=ここに楽天市場eAPIのキー

APIキー取得先
- #openwathermap：https://openweathermap.org/api
- #ぐるなび：https://api.gnavi.co.jp/api/
- #Youtube：Google Cloud Platform から YouTube Data API v3を取得
- #カーセンサー：https://webservice.recruit.co.jp/doc/carsensor/
- #News: https://newsapi.org/
- #Google: Google Cloud Platformより
- #Rakuten: https://webservice.rakuten.co.jp/api/ichibaitemsearch/

## 起動
- ./docom.sh build web
- ./docom.sh up -d
- docker exec -it django.web sh
- python manage.py migrate
- python manage.py createsuperuser

## 画面イメージ
<img src="https://user-images.githubusercontent.com/61681360/88757858-fb0b8f00-d1a1-11ea-81a3-e49f985500ae.png">
<img src="https://user-images.githubusercontent.com/61681360/88760296-b551c500-d1a7-11ea-8bbf-b1359d27478d.png">
<img src="https://user-images.githubusercontent.com/61681360/88760565-42951980-d1a8-11ea-8a9e-46fad09f731f.png">
<img src="https://user-images.githubusercontent.com/61681360/88760796-c0f1bb80-d1a8-11ea-8e9c-79f32695da66.png">
<img src="https://user-images.githubusercontent.com/61681360/88804164-7db73d00-d1e8-11ea-8955-8bc32a9fb5b0.png">
<img src="https://user-images.githubusercontent.com/61681360/88804248-9889b180-d1e8-11ea-926d-295ff3857cb8.png">
<img src="https://user-images.githubusercontent.com/61681360/88804295-ac351800-d1e8-11ea-8cbb-823aa5ec456a.png">
<img src="https://user-images.githubusercontent.com/61681360/88805176-cd4a3880-d1e9-11ea-814c-01dfccc5eed3.png">
