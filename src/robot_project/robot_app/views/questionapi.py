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
    if answer == '1':
        question.question = 'gurunavi_search'
    elif request.POST['answer'] == '2':
        question.question = 'youtube_search'
    elif request.POST['answer'] == '3':
        question.question = 'friends_search'
    elif request.POST['answer'] == '4':
        question.question = 'morning'
    elif request.POST['answer'] == '5':
        question.question = 'blog_create'
    elif request.POST['answer'] == '6':
        question.question = 'news'
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
    user_info = User_Question.objects.filter(user_name=request.user)
    address = GNAVI_Question.objects.filter(question='address', user_name=request.user).first()
    # prefecture = address.answer
    # city_name = search(prefecture)
    city_name = 'Tokyo'
    app_id = settings.API_KEY
    URL = "https://api.openweathermap.org/data/2.5/weather?q={0},jp&units=metric&lang=ja&appid={1}".format(
        city_name, app_id)

    response = requests.get(URL)
    data = response.json()

    weather = data["weather"][0]["description"]  # 最高気温
    icon = data["weather"][0]["icon"]
    temp_max = data["main"]["temp_max"]  # 最低気温
    temp_min = data["main"]["temp_min"]  # 寒暖差
    diff_temp = temp_max - temp_min  # 湿度
    humidity = data["main"]["humidity"]
    # 日付と曜日の取得
    today = datetime.datetime.now()
    date_time = today.strftime("%Y年%m月%d日 ")
    # locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    locale.setlocale(locale.LC_ALL, '')
    now_w = "{0:%A}".format(today)
    day = date_time + now_w

    context = {"場所": city_name, "日付": day, "": icon, "最高気温": str(temp_max) + "度",
               "最低気温": str(temp_min) + "度", "湿度": str(humidity) + "%"}
    return context




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