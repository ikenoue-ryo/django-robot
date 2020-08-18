import urllib
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from newsapi import NewsApiClient
from django.shortcuts import render
from django.contrib import messages
from robot_app.models import User_Question, Youtube_Question, GNAVI_Question, Robot_Evaluation, Blog, News, Net_Shop, ChatBot
from users.models import User
from django.shortcuts import redirect
from robot_project import settings
from bs4 import BeautifulSoup
import requests
import json
from googleapiclient.discovery import build
from robot_app.views import questionapi
from urllib.parse import urlencode
import datetime
from datetime import date
from datetime import datetime
from django.views import generic
from . import mixins
from ..forms import ScheduleForm
from ..models import Schedule
from django.utils import timezone
from django.http import JsonResponse


def indexfunc(request):
    thanks = ''
    answer = ''
    youtube_records = ''
    question_type = ''
    question_mesg = ''

    #ユーザーのfavorite_foodフィールドが存在すればロボットが常に質問する処理
    user = User.objects.get(id=request.user.id)
    user_first_question = User_Question.objects.filter(question='family', user_name=request.user)
    if user_first_question.exists():
        if request.method == 'POST':
            if request.POST.get('star'):
                robot = Robot_Evaluation()
                robot.robot_name = request.POST['robot_name']
                robot.score = request.POST['star']
                robot.user_name = request.user
                robot.save()
            if request.POST.get('ng_robot'):
                robot = Robot_Evaluation()
                robot.robot_name = request.POST['robot_name']
                robot.score = '0'
                robot.user_name = request.user
                robot.save()
            #リダイレクトさせる
            if request.POST.get('answer') == '1' or request.POST.get('answer') == 'ぐるなび':
                questionapi.selectAnswer(request, answer)
                return redirect('/g_navi/')
            if request.POST.get('answer') == '2' or request.POST.get('answer') == 'Youtube':
                questionapi.selectAnswer(request, answer)
                return redirect('/youtube/')
            if request.POST.get('answer') == '3' or request.POST.get('answer') == '質問':
                questionapi.selectAnswer(request, answer)
                return redirect('/add_questions')
            if request.POST.get('answer') == '4' or request.POST.get('answer') == '朝のtoDo':
                questionapi.selectAnswer(request, answer)
                return redirect('/morning')
            if request.POST.get('answer') == '5' or request.POST.get('answer') == 'ブログ':
                questionapi.selectAnswer(request, answer)
                return redirect('/blog_create')
            if request.POST.get('answer') == '6' or request.POST.get('answer') == 'ニュース':
                questionapi.selectAnswer(request, answer)
                return redirect('/news')
            if request.POST.get('answer') == '7' or request.POST.get('answer') == '予定':
                questionapi.selectAnswer(request, answer)
                return redirect('/mycalendar')
            if request.POST.get('answer') == '8' or request.POST.get('answer') == 'お出かけ':
                questionapi.selectAnswer(request, answer)
                return redirect('/map')
            if request.POST.get('answer') == '9' or request.POST.get('answer') == 'お買い物':
                questionapi.selectAnswer(request, answer)
                return redirect('/net_shop')
        else:
            #天気を表示
            tenki_api = questionapi.tenki_api(request)

            # FoursquareAPIを使う場合
            # import foursquare
            #
            # # 作成したアプリの情報を設定
            # CLIENT_ID =  ''
            # CLIENT_SECRET =  ''
            # REDIRECT_URI =  'http://localhost:8080/redirect'
            #
            # # clientオブジェクトを作成
            # client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
            #
            # # アプリの認証
            # auth_uri = client.oauth.auth_url()
            # print('値', auth_uri)
            #
            # # 表示されたauth_uriにブラウザからアクセスし、URIの「?code=」の後から「#」の前までの文字列を入力
            # code = ""
            # # アクセストークンを取得
            # access_token = client.oauth.get_token(code)
            # print('アクセストークン', access_token)
            #
            # # アクセストークンを設定
            # client.set_access_token(access_token)
            #
            # # 試しに自分のユーザ情報出力する
            # # ユーザ情報が表示されたら無事成功
            # user = client.users()
            #
            # venue_id = '4b5bb91cf964a520451229e3';
            # params = {}
            # params['oauth_token'] = access_token
            # params['locale'] = 'ja'
            # params['m'] = 'swarm'
            # params['v'] = '20150801'
            #
            # Url = 'https://api.foursquare.com/v2/venues/'
            #
            # #Jsonデータの取得
            # result_api = Url + venue_id + '?' + urllib.parse.urlencode(params)
            #
            # print('キー', result_api)
            #
            # result = requests.get(result_api)
            # result_api = result.json()
            # print(result_api)
            #
            # foursquare_records = result_api['response']['venue']
            # prefix = result_api['response']['venue']['photos']['groups'][0]['items'][0]['prefix']
            # suffix = result_api['response']['venue']['photos']['groups'][0]['items'][0]['suffix']
            #
            # photos_records = prefix + '300x300' + suffix

            annai_robot = Robot_Evaluation.objects.filter(robot_name='annai_robot', user_name=request.user).last()
            address = GNAVI_Question.objects.filter(question='address', user_name=request.user).first()

            return render(request, 'robot_app/wants.html', {
                'address': address,
                'nav_menu': '何をしたいですか？',
                'gurunavi_search': 'ぐるなび',
                'youtube_search': 'Youtube',
                'add_questions': '質問',
                'morning': '朝のtoDo',
                'blog': 'ブログ',
                'news': 'ニュース',
                'schedule': '予定',
                'map': 'お出かけ',
                'net_shop': 'お買い物',
                'type': question_type,
                'mesg': question_mesg,
                'tenki_api': tenki_api,
                'youtube_records': youtube_records,
                'annai_robot': annai_robot,
                # 'foursquare_records': foursquare_records,
                # 'photos_records': photos_records,
            })
    # ユーザーのfavorite_foodが存在しない場合、初回の質問をする
    else:
        ## 1回しか聞かない質問
        if request.method == 'POST':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
        ### 2回目以降の質問
        if request.method == 'POST':
            question_type, question_mesg = questionapi.firstQuestion(request, request.POST['question'])
        else:
            ### 初回質問
            question_type = 'favorite_food'
            question_mesg = '好きな食べ物はなんですか？'


    return render(request, 'robot_app/index.html', {
        'type': question_type,
        'mesg': question_mesg,
        'thanks': thanks,
    })


def detailfunc(request, pk):
    user = User.objects.get(id=pk)
    #ユーザー基本情報
    questions = User_Question.objects.filter(user_name=request.user)
    # addressはあえてGNAVI_Questionを使用
    address = GNAVI_Question.objects.filter(question='address', user_name=request.user).first()
    favorite_food = User_Question.objects.filter(question='favorite_food', user_name=request.user).first()
    age = User_Question.objects.filter(question='age', user_name=request.user).first()
    family = User_Question.objects.filter(question='family', user_name=request.user).first()
    favorite_sports = User_Question.objects.filter(question='favorite_sports', user_name=request.user).first()
    height = User_Question.objects.filter(question='height', user_name=request.user).first()
    weight = User_Question.objects.filter(question='weight', user_name=request.user).first()
    cleanliness = User_Question.objects.filter(question='cleanliness', user_name=request.user).first()
    mycar = User_Question.objects.filter(question='mycar', user_name=request.user).first()
    car_brand = User_Question.objects.filter(question='car_brand', user_name=request.user).first()
    wake_up = User_Question.objects.filter(question='wake_up', user_name=request.user).first()
    going_work = User_Question.objects.filter(question='going_work', user_name=request.user).first()
    nearest_station = User_Question.objects.filter(question='nearest_station', user_name=request.user).first()
    arrival_station = User_Question.objects.filter(question='arrival_station', user_name=request.user).first()
    todo_morning = User_Question.objects.filter(question='todo_morning', user_name=request.user)[0:5]
    celebrity = News.objects.filter(question='celebrity', user_name=request.user).last()
    interest = News.objects.filter(question='interest', user_name=request.user)[0:3]


    #ユーザー抜粋データ
    ##ぐるなび検索回数
    gurunavi_search_count = GNAVI_Question.objects.filter(question='keyword', user_name=request.user).count()
    ##ぐるなび検索キーワード
    gurunavi_key = GNAVI_Question.objects.filter(question='keyword', user_name=request.user)
    ##Youtube検索回数
    youtube_search_count = Youtube_Question.objects.filter(question='keyword', user_name=request.user).count()
    ##Youtube検索キーワード
    youtube_key = Youtube_Question.objects.filter(question='keyword', user_name=request.user)


    context = {
        'users': user,
        'questions': questions,
        'address': address,
        'favorite_food': favorite_food,
        'age': age,
        'family': family,
        'favorite_sports': favorite_sports,
        'height': height,
        'weight': weight,
        'cleanliness': cleanliness,
        'mycar': mycar,
        'car_brand': car_brand,
        'wake_up': wake_up,
        'going_work': going_work,
        'nearest_station': nearest_station,
        'arrival_station': arrival_station,
        'todo_morning': todo_morning,
        'celebrity': celebrity,
        'interest': interest,
        'gurunavi_search_count': gurunavi_search_count,
        'gurunavi_key': gurunavi_key,
        'youtube_search_count': youtube_search_count,
        'youtube_key': youtube_key,
    }
    return render(request, 'robot_app/detail.html', context)


def updatefunc(request, pk):

    user = User.objects.get(id=pk)
    # ユーザー基本情報
    questions = User_Question.objects.filter(user_name=request.user)
    #addressはあえてGNAVI_Questionを使用
    address = GNAVI_Question.objects.filter(question='address', user_name=request.user).first()
    favorite_food = User_Question.objects.filter(question='favorite_food', user_name=request.user).first()
    age = User_Question.objects.filter(question='age', user_name=request.user).first()
    family = User_Question.objects.filter(question='family', user_name=request.user).first()
    favorite_sports = User_Question.objects.filter(question='favorite_sports', user_name=request.user).first()
    height = User_Question.objects.filter(question='height', user_name=request.user).first()
    weight = User_Question.objects.filter(question='weight', user_name=request.user).first()
    cleanliness = User_Question.objects.filter(question='cleanliness', user_name=request.user).first()
    mycar = User_Question.objects.filter(question='mycar', user_name=request.user).first()
    car_brand = User_Question.objects.filter(question='car_brand', user_name=request.user).first()
    wake_up = User_Question.objects.filter(question='wake_up', user_name=request.user).first()
    going_work = User_Question.objects.filter(question='going_work', user_name=request.user).first()
    nearest_station = User_Question.objects.filter(question='nearest_station', user_name=request.user).first()
    arrival_station = User_Question.objects.filter(question='arrival_station', user_name=request.user).first()

    if request.method == 'POST':
        # addressはあえてGNAVI_Questionを使用
        address = GNAVI_Question.objects.filter(question='address', user_name=request.user).first()
        address.answer = request.POST['address']
        address.save()

        favorite_food = User_Question.objects.filter(question='favorite_food', user_name=request.user).first()
        favorite_food.answer = request.POST['favorite_food']
        favorite_food.save()

        age = User_Question.objects.filter(question='age', user_name=request.user).first()
        age.answer = request.POST['age']
        age.save()

        family = User_Question.objects.filter(question='family', user_name=request.user).first()
        family.answer = request.POST['family']
        family.save()

        favorite_sports = User_Question.objects.filter(question='favorite_sports', user_name=request.user).first()
        favorite_sports.answer = request.POST['favorite_sports']
        favorite_sports.save()

        cleanliness = User_Question.objects.filter(question='cleanliness', user_name=request.user).first()
        cleanliness.answer = request.POST['cleanliness']
        cleanliness.save()

        mycar = User_Question.objects.filter(question='mycar', user_name=request.user).first()
        mycar.answer = request.POST['mycar']
        mycar.save()

        car_brand = User_Question.objects.filter(question='car_brand', user_name=request.user).first()
        car_brand.answer = request.POST['car_brand']
        car_brand.save()

        wake_up = User_Question.objects.filter(question='wake_up', user_name=request.user).first()
        wake_up.answer = request.POST['wake_up']
        wake_up.save()

        going_work = User_Question.objects.filter(question='going_work', user_name=request.user).first()
        going_work.answer = request.POST['going_work']
        going_work.save()

        #値が予め入っていたら上書きし、入っていなければ新しいインスタンスを作る処理
        nearest_station = User_Question.objects.filter(question='nearest_station', user_name=request.user).first()
        if nearest_station:
            nearest_station.answer = request.POST['nearest_station']
            nearest_station.save()
        else:
            question = User_Question()
            question.question = 'nearest_station'
            question.answer = request.POST['nearest_station']
            question.user_name = request.user
            question.save()

        # 値が予め入っていたら上書きし、入っていなければ新しいインスタンスを作る処理
        arrival_station = User_Question.objects.filter(question='arrival_station', user_name=request.user).first()
        if arrival_station:
            arrival_station.answer = request.POST['arrival_station']
            arrival_station.save()
        else:
            question = User_Question()
            question.question = 'arrival_station'
            question.answer = request.POST['arrival_station']
            question.user_name = request.user
            question.save()
        return redirect('robot_app:index')

    return render(request, 'robot_app/question_edit.html', {
        'users': user,
        'questions': questions,
        'address': address,
        'favorite_food': favorite_food,
        'age': age,
        'family': family,
        'height': height,
        'weight': weight,
        'favorite_sports': favorite_sports,
        'cleanliness': cleanliness,
        'mycar': mycar,
        'car_brand': car_brand,
        'wake_up': wake_up,
        'going_work': going_work,
        'nearest_station': nearest_station,
        'arrival_station': arrival_station,
    })


def signupfunc(request):

    if request.method == 'POST':
        question_type, question_mesg = questionapi.selectQuestion(request, request.POST['question'])
        if question_type == 'thanks':
            messages.success(request, '登録が完了しました')
            return redirect('/')
    else:
        # POSTリクエストではなく、初回質問
        question_type = 'email'
        question_mesg = 'メールアドレスを教えてください'

    return render(request, 'robot_app/signup.html', {
        'type': question_type,
        'mesg': question_mesg
    })


def loginfunc(request):
    question_type = ''
    question_mesg = ''
    email = ''
    password = ''

    if request.method == 'POST':
        if request.POST['question'] == 'email':
            email = request.POST['answer']
            question_type = 'password'
            question_mesg = 'パスワードは何ですか？'
        if request.POST['question'] == 'password':
            password = request.POST['answer']
            email = request.POST['email']

        #以下でユーザーをログインさせる処理
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'ログインしました')
            return redirect('/')
    else:
        question_type = 'email'
        question_mesg = 'メールアドレスを教えてください'

    return render(request, 'robot_app/login.html', {
        'type': question_type,
        'mesg': question_mesg,
        'email': email,
    })


class Logout(LogoutView):
    template_name = 'robot_app/index.html'


info= []
def g_navi(request):
    question_type = ''
    question_mesg = ''
    freeword = ''
    g_navi_params = ''
    gnavi_records = ''

    if request.method == 'POST':
        question = GNAVI_Question()
        question.question = request.POST['question']
        question.answer = request.POST['answer']
        question.user_name = request.user
        question.save()
        if request.POST['question'] == 'address':
            city = request.POST['answer']
            question_type = 'keyword'
            question_mesg = 'キーワードを入力してください'
            info.append(city)
        if request.POST['question'] == 'keyword':
            freeword = request.POST['answer']
            info.append(freeword)
            question_type = 'thanks'
            question_mesg = '検索結果を表示します。'

        #スクレイピング
        url = 'https://www.gnavi.co.jp/'
        responce = requests.get(url)

        soup = BeautifulSoup(responce.text, 'html.parser')
        elems = soup.select('#top > main > section:nth-child(6) > div > div')
        elems_all = elems[0].find_all('section')

        g_navi_params = []

        for elem in elems_all:
            element = {
                'h2_string': elem.h2.string,
                'p_string': elem.p.string,
                'img': 'https:' + elem.img['data-src'],
                'href': elem.a['href']
            }
            g_navi_params.append(element)

        #レストラン検索APIのURL
        Url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
        # パラメータの設定
        params = {}
        params['keyid'] = settings.GNAVI_API_KEY
        params['hit_per_page'] = 3
        #都道府県コードを取ってきて変換
        # params['pref'] = search(city)
        #キーワード検索
        params['freeword'] = freeword

        if freeword:
            city = info[0]
            params['pref'] = questionapi.search(city)
            # print(params['pref'])
            params['freeword'] = info[1]
            Url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
            result_api = requests.get(Url, params)
            result_api = result_api.json()
            gnavi_records = result_api['rest']
            #検索データをリセット
            info.clear()
    else:
        info.clear()
        question_type = 'address'
        question_mesg = '都道府県を入力してください'

    context = {
        'type': question_type,
        'mesg': question_mesg,
        'gnavi_records': gnavi_records,
        'g_navi_params': g_navi_params,
    }
    return render(request, 'robot_app/g_navi.html', context)


def youtube(request):
    youtube_records = ''
    question_type = ''
    question_mesg = ''

    if request.method == 'POST':
        question = Youtube_Question()
        question.question = request.POST['question']
        question.answer = request.POST['answer']
        question.user_name = request.user
        question.save()
        if request.POST['question'] == 'keyword':
            keyword = request.POST['answer']
            question_type = 'thanks'
            question_mesg = '検索結果を表示します。'

        YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        search_response = youtube.search().list(
        part='snippet',
        #検索したい文字列を指定
        q=keyword,
        #視聴回数が多い順に取得
        order='viewCount',
        #表示件数
        maxResults=3,
        type='video',
        ).execute()

        youtube_records = search_response['items']
    else:
        # 初回質問
        question_type = 'keyword'
        question_mesg = 'キーワードを入力してください'

    return render(request, 'robot_app/youtube.html', {
        'type': question_type,
        'mesg': question_mesg,
        'youtube_records': youtube_records,
    })


def add_questions(request):
    question_type = ''
    question_mesg = ''

    if request.method == 'POST':
        question = User_Question()
        question.question = request.POST['question']
        question.answer = request.POST['answer']
        question.user_name = request.user
        question.save()

        if request.POST['question'] == 'height':
            question_type = 'weight'
            question_mesg = '体重は何キロですか？'
        if request.POST['question'] == 'weight':
            question_type = 'cleanliness'
            question_mesg = '綺麗好きですか？'
        if request.POST['question'] == 'cleanliness':
            question_type = 'mycar'
            question_mesg = '車がほしいですか？'
        if request.POST['question'] == 'mycar':
            question_type = 'car_brand'
            question_mesg = '好きな車メーカーはありますか？'
        if request.POST['question'] == 'car_brand':
            question_type = 'thanks'
            question_mesg = 'ありがとうございました。'
            redirect('/')
    else:
        height = User_Question.objects.filter(question='height', user_name=request.user).first()
        weight = User_Question.objects.filter(question='weight', user_name=request.user).first()
        cleanliness = User_Question.objects.filter(question='cleanliness', user_name=request.user).first()
        mycar = User_Question.objects.filter(question='mycar', user_name=request.user).first()
        car_brand = User_Question.objects.filter(question='car_brand', user_name=request.user).first()

        if not None:
            question_type = 'no_question'
            question_mesg = 'ただいま、質問はありません。'
        if car_brand is None:
            question_type = 'car_brand'
            question_mesg = '好きな車メーカーはありますか？'
        if mycar is None:
            question_type = 'mycar'
            question_mesg = '車がほしいですか？'
        if cleanliness is None:
            question_type = 'cleanliness'
            question_mesg = '綺麗好きですか？'
        if weight is None:
            question_type = 'weight'
            question_mesg = '体重は何キロですか？'
        if height is None:
            # 初回質問
            question_type = 'height'
            question_mesg = '身長は何センチですか？'

    return render(request, 'robot_app/add_questions.html', {
        'number': '1.はい  2.いいえ',
        'car_brand': '1. トヨタ 2.ホンダ 3.スズキ 4.マツダ 車種名など',
        'type': question_type,
        'mesg': question_mesg,
        'thanks': question_mesg
    })



def morning(request):
    wake_up = ''
    going_work = ''
    nearest_station = ''
    arrival_station = ''
    todo_morning = ''
    eki_record = ''
    near_lat = ''
    near_lng = ''
    arri_lat = ''
    arri_lng = ''
    Google_api_key = ''
    question_type = ''
    question_mesg = ''

    if request.method == 'POST':
        if request.POST['question'] == 'wake_up':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
            question_type = 'going_work'
            question_mesg = '何時に家をでますか？'
        if request.POST['question'] == 'going_work':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
            question_type = 'nearest_station'
            question_mesg = '最寄駅はどこですか？'
        if request.POST['question'] == 'nearest_station':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
            question_type = 'arrival_station'
            question_mesg = '到着駅はどこですか？'
        if request.POST['question'] == 'arrival_station':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
            question_type = 'todo_morning'
            question_mesg = '朝のやることリストを作成しよう'
        if request.POST['question'] == 'todo_morning':
            question = User_Question()
            question.question = request.POST['question']
            question.answer  = request.POST['answer1']
            question.user_name = request.user
            question.save()

            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer2']
            question.user_name = request.user
            question.save()

            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer3']
            question.user_name = request.user
            question.save()
            question_type = 'thanks'
            question_mesg = 'ありがとうございました。'
            redirect('/')
    else:


        nearest_station = User_Question.objects.filter(question='nearest_station', user_name=request.user).first()
        arrival_station = User_Question.objects.filter(question='arrival_station', user_name=request.user).first()

        if nearest_station:
            #駅の文字列を削除しAPIパラメータ加工
            near_sta = nearest_station.answer
            arri_sta = arrival_station.answer
            near_sta = near_sta.replace('駅', '')
            arri_sta = arri_sta.replace('駅', '')

            params = {}
            params['key'] = settings.EKISPART_API_KEY
            params['from'] = near_sta
            params['to'] = arri_sta

            Url = 'http://api.ekispert.jp/v1/json/search/course/light?key='+settings.NEWS_API_KEY
            result_api = requests.get(Url, params)
            result_api = result_api.json()
            eki_record = result_api['ResultSet']['ResourceURI']


        wake_up = User_Question.objects.filter(question='wake_up', user_name=request.user).last()
        going_work = User_Question.objects.filter(question='going_work', user_name=request.user).last()
        nearest_station = User_Question.objects.filter(question='nearest_station', user_name=request.user).last()
        arrival_station = User_Question.objects.filter(question='arrival_station', user_name=request.user).last()
        todo_morning = User_Question.objects.order_by('id').reverse().filter(question='todo_morning',
                                                                             user_name=request.user)[0:3]

        if not None:
            question_type = 'no_question'
            question_mesg = 'ただいま、質問はありません。'
        if todo_morning is None:
            question_type = 'todo_morning'
            question_mesg = '朝のやることリストを作成しよう'
        if going_work is None:
            question_type = 'arrival_station'
            question_mesg = '到着駅はどこですか？'
        if going_work is None:
            question_type = 'nearest_station'
            question_mesg = '最寄駅はどこですか？'
        if going_work is None:
            question_type = 'going_work'
            question_mesg = '何時に家をでますか？'
        if wake_up is None:
            # 初回質問
            question_type = 'wake_up'
            question_mesg = '平日は何時に起きますか？'

        nearest_station = User_Question.objects.filter(question='nearest_station', user_name=request.user).last()
        arrival_station = User_Question.objects.filter(question='arrival_station', user_name=request.user).last()
        if arrival_station:
            address1 = nearest_station.answer
            address2 = arrival_station.answer

            Url = 'https://maps.googleapis.com/maps/api/geocode/json?address=APIキー'
            #Jsonデータの取得
            result_api = Url + address1 + 'components=country:JP&key=' + settings.Google_API_KEY
            result_api2 = Url + address2 + 'components=country:JP&key=' + settings.Google_API_KEY
            result = requests.get(result_api)
            result2 = requests.get(result_api2)
            result_api = result.json()
            result_api2 = result2.json()
            near_lat = result_api['results'][0]['geometry']['location']['lat']
            near_lng = result_api['results'][0]['geometry']['location']['lng']
            arri_lat = result_api2['results'][0]['geometry']['location']['lat']
            arri_lng = result_api2['results'][0]['geometry']['location']['lng']

            Google_api_key = settings.Google_API_KEY

    return render(request, 'robot_app/morning.html', {
        'wake_up': wake_up,
        'going_work': going_work,
        'nearest_station': nearest_station,
        'arrival_station': arrival_station,
        'todo_morning': todo_morning,
        'eki_record': eki_record,
        'near_lat': near_lat,
        'near_lng': near_lng,
        'arri_lat': arri_lat,
        'arri_lng': arri_lng,
        'Google_api_key': Google_api_key,
        'type': question_type,
        'mesg': question_mesg,
        'thanks': question_mesg
    })


def morning_edit(request, pk):

    wake_up = ''
    going_work = ''
    nearest_station = ''
    arrival_station = ''
    todo_morning = ''
    question_type = ''
    question_mesg = ''

    if request.method == 'POST':
        if request.POST['question'] == 'wake_up':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
            question_type = 'going_work'
            question_mesg = '何時に家をでますか？'
        if request.POST['question'] == 'going_work':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
            question_type = 'nearest_station'
            question_mesg = '最寄駅はどこですか？'
        if request.POST['question'] == 'nearest_station':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
            question_type = 'arrival_station'
            question_mesg = '到着駅はどこですか？'
        if request.POST['question'] == 'arrival_station':
            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer']
            question.user_name = request.user
            question.save()
            question_type = 'todo_morning'
            question_mesg = '朝のやることリストを作成しよう'

        if request.POST['question'] == 'todo_morning':
            question = User_Question()
            question.question = request.POST['question']
            question.answer  = request.POST['answer1']
            question.user_name = request.user
            question.save()

            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer2']
            question.user_name = request.user
            question.save()

            question = User_Question()
            question.question = request.POST['question']
            question.answer = request.POST['answer3']
            question.user_name = request.user
            question.save()
            question_type = 'thanks'
            question_mesg = 'ありがとうございました。'
            redirect('/')
    else:
            # 初回質問
            question_type = 'wake_up'
            question_mesg = '平日は何時に起きますか？'


    return render(request, 'robot_app/morning_edit.html', {
        'wake_up': wake_up,
        'going_work': going_work,
        'nearest_station': nearest_station,
        'arrival_station': arrival_station,
        'todo_morning': todo_morning,
        'type': question_type,
        'mesg': question_mesg,
        'thanks': question_mesg
    })


def blog_create(request):
    blogs = Blog.objects.filter(user_name=request.user).order_by('-created_at')

    if request.method == 'POST':
        blog = Blog()
        blog.title  = request.POST['title']
        blog.text  = request.POST['text']
        blog.user_name = request.user
        blog.save()
        question_type = 'thanks'
        question_mesg = 'ブログを作成しました。'
        redirect('/')
    else:
        # 初回質問
        question_type = 'blog'
        question_mesg = 'ブログを書きましょう！'


    return render(request, 'robot_app/blog.html', {
        'blogs': blogs,
        'type': question_type,
        'mesg': question_mesg,
        'thanks': question_mesg
    })


def news(request):

    categories = ''
    sports = ''
    originals = ''
    technologys = ''

    if request.method == 'POST':

        if request.POST['question'] == 'celebrity':
            news = News()
            news.question = request.POST['question']
            news.answer = request.POST['answer']
            news.user_name = request.user
            news.save()
            question_type = 'interest'
            question_mesg = 'どんなカテゴリが好きですか？'
        if request.POST['question'] == 'interest':
            values = request.POST.getlist('answer')
            if 'general' in values:
                news = News()
                news.question = request.POST['question']
                news.answer = 'general'
                news.user_name = request.user
                news.save()
            if 'entertainment' in values:
                news = News()
                news.question = request.POST['question']
                news.answer = 'entertainment'
                news.user_name = request.user
                news.save()
            if 'business' in values:
                news = News()
                news.question = request.POST['question']
                news.answer = 'business'
                news.user_name = request.user
                news.save()
            if 'health' in values:
                news = News()
                news.question = request.POST['question']
                news.answer = 'health'
                news.user_name = request.user
                news.save()
            if 'science' in values:
                news = News()
                news.question = request.POST['question']
                news.answer = 'science'
                news.user_name = request.user
                news.save()
            if 'technology' in values:
                news = News()
                news.question = request.POST['question']
                news.answer = 'technology'
                news.user_name = request.user
                news.save()

            question_type = 'thanks'
            question_mesg = '記事を表示します。'
            redirect('/')
    else:
        # 初回質問
        question_type = 'celebrity'
        question_mesg = '好きなタレントは誰ですか？'


    celebrity = News.objects.filter(question='celebrity', user_name=request.user).last()
    if celebrity:
        celebrity_name = celebrity.answer

        newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

        categories = newsapi.get_top_headlines(category='entertainment',
                                              country='jp',
                                              page_size=20,
                                              )
        sports = newsapi.get_top_headlines(category='sports',
                                              country='jp',
                                              page_size=7,
                                              )
        if originals:
            originals = newsapi.get_top_headlines(q=celebrity_name,
                                                  country='jp',
                                                  page_size=7,
                                                  )
        else:
            technologys = newsapi.get_top_headlines(category='technology',
                                                  country='jp',
                                                  page_size=7,
                                                  )


        #API表示
        categories = categories['articles']
        sports = sports['articles']
        technologys = technologys['articles']
        if originals:
            originals = originals['articles']

    return render(request, 'robot_app/news.html', {
        'general': '一般',
        'business': 'ビジネス',
        'entertainment': 'エンタメ',
        'health': '健康',
        'science': 'サイエンス',
        'technology': 'テクノロジー',
        'categories': categories,
        'sports': sports,
        'originals': originals,
        'technologys': technologys,
        'type': question_type,
        'mesg': question_mesg,
        'thanks': question_mesg
    })


class MyCalendar(mixins.MonthCalendarMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'robot_app/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        date = form.cleaned_data['date']
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.user_name = self.request.user
        schedule.save()
        return redirect('robot_app:month_with_schedule')


class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'robot_app/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    template_name = 'robot_app/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


def map(request):

    if request.method == 'POST':
        question = GNAVI_Question()
        question.question = request.POST['question']
        question.answer = request.POST['answer']
        question.user_name = request.user
        question.save()
        if request.POST['question'] == 'address':
            city = request.POST['answer']
            question_type = 'keyword'
            question_mesg = 'キーワードを入力してください'
            info.append(city)
        if request.POST['question'] == 'keyword':
            freeword = request.POST['answer']
            info.append(freeword)
            question_type = 'thanks'
            question_mesg = '検索結果を表示します。'

        #レストラン検索APIのURL
        Url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
        # パラメータの設定
        params = {}
        params['keyid'] = settings.GNAVI_API_KEY
        params['hit_per_page'] = 3
        #都道府県コードを取ってきて変換
        # params['pref'] = search(city)
        #キーワード検索
        params['freeword'] = freeword


        if freeword:
            city = info[0]
            params['pref'] = questionapi.search(city)
            print(params['pref'])
            params['freeword'] = info[1]
            Url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
            result_api = requests.get(Url, params)
            result_api = result_api.json()
            gnavi_records = result_api['rest']
            #検索データをリセット
            info.clear()
    else:
        question_type = 'address'
        question_mesg = '都道府県を入力してください'



    context = {
        'type': question_type,
        'mesg': question_mesg,
        # 'gnavi_records': gnavi_records
    }
    return render(request, 'robot_app/map.html', context)


def robot_review(request):
    robot_query = Robot_Evaluation.objects.filter(user_name=request.user)

    context = {
        'robot_query': robot_query
        # 'type': question_type,
        # 'mesg': question_mesg,
    }
    return render(request, 'robot_app/robot_review.html', context)



def notify(request):

    carnews_show_eva = ''
    not_show_eva = ''
    carnews_not_show_eva = ''
    health_show_eva = ''
    health_not_show_eva = ''
    weight_result = ''
    weight = ''
    suitable_weight = ''
    overweight = ''
    overweight_text = ''
    carsensor_records = ''
    carsensor_records_ver2 = ''
    car_news = ''
    add_car_news = ''

    # カーセンサーを表示
    car_brand = User_Question.objects.filter(question='car_brand', user_name=request.user).first()
    if car_brand:
        if car_brand.answer == '1':
            car_brand.answer = 'トヨタ'
        elif car_brand.answer == '2':
            car_brand.answer = 'ホンダ'
        elif car_brand.answer == '3':
            car_brand.answer = 'スズキ'
        elif car_brand.answer == '4':
            car_brand.answer = 'マツダ'
        else:
            car_brand.answer = car_brand.answer

        # ユーザーの好きなメーカーの車を表示する処理
        url = "http://webservice.recruit.co.jp/carsensor/usedcar/v1/?{}".format(
            urlencode({
                'key': settings.CARSENSOR_API_KEY,
                # "keyword": "HONDA S660",
                'keyword': car_brand.answer,
                # 表示件数
                'count': 3,
                'format': 'json'
            }))

        fu = requests.get(url).content
        json_result = json.loads(fu)

        carsensor_records = json_result['results']['usedcar']
        user = User.objects.get(id=request.user.id)
        car_news = str(user.profname) + 'さんにおすすめ情報があります！'

        # 家族の人数から乗員を満たした車を案内する処理
        family = User_Question.objects.filter(question='family', user_name=request.user).first()
        url = "http://webservice.recruit.co.jp/carsensor/usedcar/v1/?{}".format(
            urlencode({
                'key': settings.CARSENSOR_API_KEY,
                # "keyword": "例：HONDA S660",
                'keyword': car_brand.answer,
                # 表示件数
                'count': 3,
                'person': family.answer,
                'format': 'json'
            }))
        ho = requests.get(url).content
        json_result = json.loads(ho)

        carsensor_records_ver2 = json_result['results']['usedcar']
        add_car_news = 'たしか、' + str(user.profname) + 'さんは家族が' + family.answer + '人でしたね？\n' + \
                       family.answer + '人乗りの車もご紹介しておきます。'

        carnews_robot = Robot_Evaluation.objects.filter(robot_name='carnews_robot', user_name=request.user)
        if carnews_robot:
            # ロボットが存在していない時とゼロじゃないなら表示する
            for carnews_robot_evaluation in carnews_robot:
                # ロボットの評価が存在していてゼロ(削除)されていないなら
                if carnews_robot_evaluation.score != 0:
                    carnews_show_eva = carnews_robot
                else:
                    carnews_not_show_eva = carnews_robot
        else:
            # ロボットの評価がない時でも表示する
            carnews_show_eva = carnews_robot

    # ロボットの種類
    annai_robot = Robot_Evaluation.objects.filter(robot_name='annai_robot', user_name=request.user).last()
    carnews_robot = Robot_Evaluation.objects.filter(robot_name='carnews_robot', user_name=request.user).last()
    healthy_robot = Robot_Evaluation.objects.filter(robot_name='healthy_robot', user_name=request.user).last()
    schedule_robot = Robot_Evaluation.objects.filter(robot_name='schedule_robot', user_name=request.user).last()

    #体重の検査
    height = User_Question.objects.filter(question='height', user_name=request.user).first()
    if height:
        height = int(height.answer) / 100
        #適性体重
        suitable_weight = height * height * 22
        #現在の体重 weight.answer
        weight = User_Question.objects.filter(question='weight', user_name=request.user).first()
        #超過分
        overweight = int(weight.answer) - round(suitable_weight)

        if int(weight.answer) >= round(suitable_weight):
            weight_result = '少し運動をした方が良いかも。'
            overweight_text = '標準体重より' + str(overweight) + 'キロ太っています。'

        #体重から太っている人にYoutubeでダイエット動画を提供
        # YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY
        # youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        #
        # search_response = youtube.search().list(
        #     part='snippet',
        #     # 検索したい文字列を指定
        #     q='ダイエット',
        #     # 表示件数
        #     maxResults=1,
        #     # 視聴回数が多い順に取得
        #     order='viewCount',
        #     type='video',
        # ).execute()

        # youtube_records = search_response['items']

    health_robot = Robot_Evaluation.objects.filter(robot_name='healthy_robot', user_name=request.user)
    if health_robot:
        # ロボットが存在していない時とゼロじゃないなら表示する
        for health_robot_evaluation in health_robot:
            # ロボットの評価が存在していてゼロ(削除)されていないなら
            if health_robot_evaluation.score != 0:
                health_show_eva = health_robot
            else:
                health_not_show_eva = health_robot
    else:
        # ロボットの評価がない時でも表示する
        health_show_eva = health_robot


    # スケジュール機能
    today = timezone.now().date()
    schedule_records = Schedule.objects.order_by('date').filter(date=today, user_name=request.user)

    eva = Robot_Evaluation.objects.filter(robot_name='schedule_robot', user_name=request.user)

    if eva:
        print('ロボットの評価がされています、1以上か削除のどちらかです')
        # ロボットが存在していない時とゼロじゃないなら表示する
        for evaluation in eva:
            # ロボットの評価が存在していてゼロ(削除)されていないなら
            if evaluation.score != 0:
                show_eva = eva
                print('表示します')
            else:
                not_show_eva = eva
                print('表示しません')
    else:
        print('ロボットの評価がありません。表示します')
        # ロボットの評価がない時でも表示する
        show_eva = eva

    # 件数カウント
    notify_count = 0
    if carsensor_records:
        notify_count += 1
    if overweight:
        notify_count += 1
    if schedule_records:
        notify_count += 1

    context = {
        'show_eva': show_eva,
        'not_show_eva': not_show_eva,
        'eva': eva,
        'weight_result': weight_result,
        'weight': weight,
        'suitable_weight': suitable_weight,
        'overweight': overweight,
        'overweight_text': overweight_text,
        'carsensor_records': carsensor_records,
        'car_news': car_news,
        'add_car_news': add_car_news,
        'carsensor_records_ver2': carsensor_records_ver2,
        'carnews_show_eva': carnews_show_eva,
        'carnews_not_show_eva': carnews_not_show_eva,
        'health_show_eva': health_show_eva,
        'notify_count': notify_count,
        'health_not_show_eva': health_not_show_eva,
        'schedule_records': schedule_records,
        'carnews_robot': carnews_robot,
        'annai_robot': annai_robot,
        'healthy_robot': healthy_robot,
        'schedule_robot': schedule_robot,
        # 'type': question_type,
        # 'mesg': question_mesg,
    }
    return render(request, 'robot_app/notify.html', context)


def week_tenki(request):
    # 天気を表示
    week_tenki = questionapi.tenki_api(request)

    API_Key = settings.API_KEY
    city = 'Tokyo,jp'
    url = 'http://api.openweathermap.org/data/2.5/forecast'

    query = {
        'units': 'metric',
        'q': city,
        'cnt': '30',
        'appid': API_Key
    }

    r = requests.get(url, params=query)
    #week
    result = (r.json()['list'])
    print('テスト1', result)

    for i in range(r.json()['cnt']):
        all_day = (result[i]['dt_txt'])
        result[i]['dt_txt'] = datetime.strptime(all_day, "%Y-%m-%d %H:%M:%S")

    result_date1 = result[0]['dt_txt']
    result_date2 = result[8]['dt_txt']
    result_date3 = result[16]['dt_txt']
    result_date4 = result[24]['dt_txt']

    context = {
        'week_tenki': week_tenki,
        'result': result,
        'result_day1': result[0],
        'result_day2': result[8],
        'result_day3': result[16],
        'result_day4': result[24],
        'result_date1': result_date1,
        'result_date2': result_date2,
        'result_date3': result_date3,
        'result_date4': result_date4,
    }

    return render(request, 'robot_app/week_tenki.html', context)


def net_shop(request):

    if request.method == 'POST':
        if request.POST['question'] == 'want_object':
            news = Net_Shop()
            news.question = request.POST['question']
            news.answer = request.POST['answer']
            news.user_name = request.user
            news.save()
            question_type = 'object_category'
            question_mesg = 'どんなカテゴリが好きですか？'
        if request.POST['question'] == 'object_category':
            values = request.POST.getlist('answer')
            if 'mens' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'mens'
                net_shop.user_name = request.user
                net_shop.save()
            if 'women' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'women'
                net_shop.user_name = request.user
                net_shop.save()
            if 'shoes' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'shoes'
                net_shop.user_name = request.user
                net_shop.save()
            if 'bag' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'bag'
                net_shop.user_name = request.user
                net_shop.save()
            if 'underwear' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'underwear'
                net_shop.user_name = request.user
                net_shop.save()
            if 'jewelry' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'jewelry'
                net_shop.user_name = request.user
                net_shop.save()
            if 'drink' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'drink'
                net_shop.user_name = request.user
                net_shop.save()
            if 'food' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'food'
                net_shop.user_name = request.user
                net_shop.save()
            if 'beer' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'beer'
                net_shop.user_name = request.user
                net_shop.save()
            if 'sake' in values:
                net_shop = Net_Shop()
                net_shop.question = request.POST['question']
                net_shop.answer = 'sake'
                net_shop.user_name = request.user
                net_shop.save()

            question_type = 'thanks'
            question_mesg = '商品を表示します。'
            redirect('/')
    else:
        # 初回質問
        question_type = 'want_object'
        question_mesg = '何かほしいものはありますか？'

    item_records = questionapi.kick_rakten_api()
    item_records = item_records['item_records']

    return render(request, 'robot_app/net_shop.html', {
        'mens': 'メンズファッション',
        'women': 'レディースファッション',
        'shoes': '靴',
        'bag': 'バッグ・小物・ブランド・雑貨',
        'underwear': '下着・ナイトウェア',
        'jewelry': 'ジュエリー・アクセサリー',
        'drink': '水・ソフトドリンク',
        'food': '食品',
        'beer': 'ビール',
        'sake': '日本酒',
        'item_records': item_records,
        'type': question_type,
        'mesg': question_mesg,
        'thanks': question_mesg
    })


def shop_detail(request, itemId):

    item_records = questionapi.itemcode_rakten_api(itemId)
    item_records = item_records['item_records']['Items'][0]['Item']

    return render(request, 'robot_app/shop_detail.html', {
        'item_records': item_records,
    })


def any_questions(request):
    non_answer = ChatBot.objects.filter(answer__isnull=True).first()

    # 回答済みの質問
    answered = ChatBot.objects.filter(answer__isnull=False).first()

    return render(request, 'robot_app/chatbot.html', {
        # 未回答
        'non_answer': non_answer,
        # 未回答の質問
        'answer_question': non_answer.question,
        # 回答済み
        # 'answered_list': answered_list,
        'answered': answered
    })


def ajax_answer_add(request):
    question = request.POST.get('question')
    answer = request.POST.get('answer')
    username = request.user
    print('1:',question)
    print('2:',answer)
    print('3:',username)

    question_obj = ChatBot.objects.get(question=question)
    question_obj.answer = answer
    question_obj.user_name = username
    question_obj.save()

    next_question = ChatBot.objects.filter(answer__isnull=True).first()

    d = {
        'question': question_obj.question,
        'answer': question_obj.answer,
        'next_question': next_question.question
    }
    print(d)

    return JsonResponse(d)