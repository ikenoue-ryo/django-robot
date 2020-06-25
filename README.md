# チャットロボット
会話型ロボット

## バージョン
- Python 3.7.3
- Django 3.0.7

## 起動
1. git clone url
2. pipenv shell
3. pipenv install django
4. touch settings_local.py　ファイル内記述：SECRET_KEY = 'xxxxxxxxxxxxxx'
5. touch .env　
** .envファイル内記述 **
------------------------------------
- API_KEY=ここにopenweathermapのAPIキー 　#取得先：https://openweathermap.org/api

- GNAVI_API_KEY=ここにぐるなびのAPIキー 　#取得先：https://api.gnavi.co.jp/api/

- YOUTUBE_API_KEY=ここにYoutubeのAPIキー 　#取得先：Google Cloud Platform から YouTube Data API v3を取得
------------------------------------------------
6. python manage.py migrate
7. python manage.py runserver