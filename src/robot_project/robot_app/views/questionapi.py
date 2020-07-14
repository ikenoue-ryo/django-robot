from django.shortcuts import render, redirect
from users.models import User
from robot_app.models import User_Question, Youtube_Question, GNAVI_Question
from django.contrib.auth import login, authenticate
from robot_project import settings
import requests
import datetime
import locale
import json
import urllib.request
import time
from urllib.parse import urlencode
from . import views


#indexfunc
def selectAnswer(request, answer):
    question = User_Question()
    if answer == '1' or answer == 'ぐるなび':
        question.question = 'gurunavi_search'
    elif request.POST['answer'] == '2' or request.POST['answer'] == 'Youtube':
        question.question = 'youtube_search'
    elif request.POST['answer'] == '3' or request.POST['answer'] == '質問':
        question.question = 'friends_search'
    elif request.POST['answer'] == '4' or request.POST['answer'] == '朝のtoDo':
        question.question = 'morning'
    elif request.POST['answer'] == '5' or request.POST['answer'] == 'ブログ':
        question.question = 'blog_create'
    elif request.POST['answer'] == '6' or request.POST['answer'] == 'ニュース':
        question.question = 'news'
    elif request.POST['answer'] == '7' or request.POST['answer'] == '予定':
        question.question = 'mycalendar'
    elif request.POST['answer'] == '8' or request.POST['answer'] == 'お出かけ':
        question.question = 'map'
    else:
        question.question = 'none'
    return question.question



def firstQuestion(request, previous_question):
    question_type = ''
    question_mesg = ''

    if previous_question == 'favorite_food':
        question_type = 'favorite_sports'
        question_mesg = '好きなスポーツはなんですか？'
    elif request.POST['question'] == 'favorite_sports':
        question_type = 'age'
        question_mesg = '何歳ですか？'
    elif request.POST['question'] == 'age':
        question_type = 'family'
        question_mesg = '家族は何人ですか？'
    elif request.POST['question'] == 'family':
        question_type = 'thanks'
        question_mesg = 'ありがとうございました。'

    return (question_type, question_mesg)


#signup
def selectQuestion(request, previous_question):
    question_type = ''
    question_mesg = ''

    if previous_question == 'email':
        user = User()
        user.email = request.POST['answer']
        user.save()
        question_type = 'profname'
        question_mesg = 'ニックネームは何ですか？'
    if request.POST['question'] == 'profname':
        user = User.objects.last()
        user.profname = request.POST['answer']
        user.save()
        question_type = 'password1'
        question_mesg = 'パスワードを設定してください'
    if request.POST['question'] == 'password1':
        user = User.objects.last()
        user.password = request.POST['answer']
        user.save()
        question_type = 'password2'
        question_mesg = 'もう一度パスワードを入力してください'
    if request.POST['question'] == 'password2':
        user = User.objects.last()
        if user.password == request.POST['answer']:
            # lastに登録したユーザーをemailで取得してパスワードのみを更新する処理
            user = User.objects.get(email__exact=user.email)
            user.set_password(user.password)
            user.save()
            question_type = 'thanks'
            question_mesg = '登録が完了しました'
            return(question_type, question_mesg)
        else:
            # パスワード2が間違っていた場合の処理
            question_type = 'password2'
            question_mesg = 'パスワードが間違っています。再入力してください'
            if user.password == 'password2':
                user = User.objects.get(email__exact=user.email)
                user.set_password(user.password)
                user.save()
                return(question_type, question_mesg)
        return render(request, 'robot_app/signup.html', {
            'type': question_type,
            'mesg': question_mesg
        })

    return(question_type, question_mesg)


# 天気API表示
def tenki_api(request):
    city_name = ''
    weather = ''
    current_temperature = ''
    max_temperature = ''
    min_temperature = ''
    humidity = ''
    pressure = ''
    wind = ''

    apiKey = settings.API_KEY
    # ベースURL
    baseUrl = "http://api.openweathermap.org/data/2.5/weather?"

    #都市コード取得
    address = GNAVI_Question.objects.filter(question='address', user_name=request.user).first()
    if address:
        en_address = search_map_code(address.answer)
        # アルファベットで都市名の名前を入力
        cityName = en_address
        # URL作成
        completeUrl = baseUrl + "appid=" + apiKey + "&q=" + cityName
        # レスポンス
        response = requests.get(completeUrl)
        # レスポンスの内容をJSONフォーマットからPythonフォーマットに変換
        cityData = response.json()

        # Codが404だと都市名が見つかりませんの意味
        if cityData["cod"] != "404":
            city_name = cityData["name"]
            weather =  cityData["weather"][0]["icon"]
            current_temperature = cityData["main"]["temp"] - 273.15
            max_temperature = cityData["main"]["temp_max"] - 273.15
            min_temperature =  cityData["main"]["temp_min"] - 273.15
            #湿度
            humidity = cityData["main"]["humidity"]
            #気圧
            pressure = cityData["main"]["pressure"]
            #風速
            wind = cityData["wind"]["speed"]
        else:
            print("都市名がみつかりませんでした。")


    context = {
        'city_name': city_name,
        'weather': weather,
        'current_temperature': current_temperature,
        'max_temperature': max_temperature,
        'min_temperature': min_temperature,
        'humidity': humidity,
        'pressure': pressure,
        'wind': wind,
        }
    return context


#天気API都道府県コード
def search_map_code(city):
    tenki_dict = {
        '北海道': 'Hokkaido',
        '青森県': 'PREF02',
        '岩手県': 'PREF03',
        '宮城県': 'PREF04',
        '秋田県': 'PREF05',
        '山形県': 'PREF06',
        '福島県': 'PREF07',
        '茨城県': 'PREF08',
        '栃木県': 'PREF09',
        '群馬県': 'PREF10',
        '埼玉県': 'Saitama',
        '千葉県': 'Chiba',
        '東京都': 'Tokyo',
        '神奈川県': 'Kanagawa',
        '新潟県': 'PREF15',
        '富山県': 'PREF16',
        '石川県': 'PREF17',
        '福井県': 'PREF18',
        '山梨県': 'PREF19',
        '長野県': 'PREF20',
        '岐阜県': 'PREF21',
        '静岡県': 'PREF22',
        '愛知県': 'PREF23',
        '三重県': 'PREF24',
        '滋賀県': 'PREF25',
        '京都府': 'Kyoto',
        '大阪府': 'Osaka',
        '兵庫県': 'PREF28',
        '奈良県': 'Nara',
        '和歌山県': 'PREF30',
        '鳥取県': 'PREF31',
        '島根県': 'PREF32',
        '岡山県': 'PREF33',
        '広島県': 'Hiroshima',
        '山口県': 'PREF35',
        '徳島県': 'PREF36',
        '香川県': 'PREF37',
        '愛媛県': 'PREF38',
        '高知県': 'PREF39',
        '福岡県': 'Fukuoka',
        '佐賀県': 'Saga',
        '長崎県': 'Nagasaki',
        '熊本県': 'Kumamoto',
        '大分県': 'Oita',
        '宮崎県': 'Miyazaki',
        '鹿児島県': 'Kagoshima',
        '沖縄県': 'Okinawa',
    }
    pre_city_code = tenki_dict[city]
    return pre_city_code


#都道府県コード検索
def search(city):
    dict = {
        '北海道': 'PREF01',
        '青森県': 'PREF02',
        '岩手県': 'PREF03',
        '宮城県': 'PREF04',
        '秋田県': 'PREF05',
        '山形県': 'PREF06',
        '福島県': 'PREF07',
        '茨城県': 'PREF08',
        '栃木県': 'PREF09',
        '群馬県': 'PREF10',
        '埼玉県': 'PREF11',
        '千葉県': 'PREF12',
        '東京都': 'PREF13',
        '神奈川県': 'PREF14',
        '新潟県': 'PREF15',
        '富山県': 'PREF16',
        '石川県': 'PREF17',
        '福井県': 'PREF18',
        '山梨県': 'PREF19',
        '長野県': 'PREF20',
        '岐阜県': 'PREF21',
        '静岡県': 'PREF22',
        '愛知県': 'PREF23',
        '三重県': 'PREF24',
        '滋賀県': 'PREF25',
        '京都府': 'PREF26',
        '大阪府': 'PREF27',
        '兵庫県': 'PREF28',
        '奈良県': 'PREF29',
        '和歌山県': 'PREF30',
        '鳥取県': 'PREF31',
        '島根県': 'PREF32',
        '岡山県': 'PREF33',
        '広島県': 'PREF34',
        '山口県': 'PREF35',
        '徳島県': 'PREF36',
        '香川県': 'PREF37',
        '愛媛県': 'PREF38',
        '高知県': 'PREF39',
        '福岡県': 'PREF40',
        '佐賀県': 'PREF41',
        '長崎県': 'PREF42',
        '熊本県': 'PREF43',
        '大分県': 'PREF44',
        '宮崎県': 'PREF45',
        '鹿児島県': 'PREF46',
        '沖縄県': 'PREF47',
    }
    pre_code = dict[city]
    return pre_code


#カーセンサーAPI
def carsensor_api(request):
    url = "http://webservice.recruit.co.jp/carsensor/usedcar/v1/?{}".format(
        urlencode({
            'key': settings.CARSENSOR_API_KEY,
            # "keyword": "HONDA S660",
            'format': 'json'
             }))

    fu = requests.get(url).content
    json_result = json.loads(fu)

    # print(json_result['results']['usedcar'][0])
    # name = json_result['results']['usedcar'][0]['brand']['name']
    # odd = json_result['results']['usedcar'][0]['odd']
    # photo = json_result['results']['usedcar'][0]['photo']['main']['l']
    # photo1 = json_result['results']['usedcar'][0]['photo']['sub'][0]
    # photo2 = json_result['results']['usedcar'][0]['photo']['sub'][1]
    # photo3 = json_result['results']['usedcar'][0]['photo']['sub'][2]
    # photo4 = json_result['results']['usedcar'][0]['photo']['sub'][3]
    carsensor_records = json_result['results']['usedcar'][0]

    context = {
        # "メーカー": name,
        # "走行距離": odd,
        # "写真1": photo1,
        # "写真2": photo2,
        # "写真3": photo3,
        # "写真4": photo4,
        'carsensor_records': carsensor_records
    }
    return context