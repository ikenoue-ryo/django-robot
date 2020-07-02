from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib import messages
from robot_app.models import User_Question, Youtube_Question, GNAVI_Question
from users.models import User
from django.shortcuts import redirect
from robot_project import settings
import requests
import datetime
import locale
import json
import urllib.request
import time
from googleapiclient.discovery import build
from robot_app.views import questionapi
from urllib.parse import urlencode
from robot_app.forms import EditForm


DEFAULT_ROBOT_NAME = 'Roboko'


def indexfunc(request):
    thanks = ''
    answer = ''
    tenki_api = ''
    carsensor_records = ''
    car_news = ''
    add_car_news = ''
    carsensor_records_ver2 = ''
    weight_result = ''
    weight = ''
    suitable_weight = ''
    overweight = ''
    overweight_text = ''
    youtube_records = ''
    question_type = ''
    question_mesg = ''


    #ユーザーのfavorite_foodフィールドが存在すればロボットが常に質問する処理
    user = User.objects.get(id=request.user.id)
    user_first_question = User_Question.objects.filter(question='family', user_name=request.user)
    if user_first_question.exists():
        if request.method == 'POST':
            #何がしたいかを番号で取得する
            questionapi.selectAnswer(request, answer)
            #リダイレクトさせる
            if request.POST['answer'] == '1':
                return redirect('/g_navi/')
            if request.POST['answer'] == '2':
                return redirect('/youtube/')
            if request.POST['answer'] == '3':
                return redirect('/add_questions')
            if request.POST['answer'] == '4':
                return redirect('/morning')
        else:
            #天気を表示
            tenki_api = questionapi.tenki_api(request)

            #ぐるなび
            ## レストラン検索APIのURL
            Url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
            ## パラメータの設定
            params = {}
            params['keyid'] = settings.GNAVI_API_KEY
            params['hit_per_page'] = 1
            ## 都道府県コードを取ってきて変換
            address = GNAVI_Question.objects.filter(question='address', user_name=request.user).first()
            # prefecture = address.answer
            # params['pref'] = questionapi.search(prefecture)
            params['pref'] = 'PREF13'
            params['freeword'] = '冷たい,そば,うどん'
            Url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
            result_api = requests.get(Url, params)
            result_api = result_api.json()
            gnavi_records = result_api['rest']

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

                #ユーザーの好きなメーカーの車を表示する処理
                url = "http://webservice.recruit.co.jp/carsensor/usedcar/v1/?{}".format(
                    urlencode({
                        'key': settings.CARSENSOR_API_KEY,
                        # "keyword": "HONDA S660",
                        'keyword': car_brand.answer,
                        #表示件数
                        'count': 3,
                        'format': 'json'
                    }))

                fu = requests.get(url).content
                json_result = json.loads(fu)

                carsensor_records = json_result['results']['usedcar']
                car_news = str(user.profname) + 'さんにおすすめ情報があります！'

                #家族の人数から乗員を満たした車を案内する処理
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

                # search_response = youtube.search().list(
                #     part='snippet',
                #     # 検索したい文字列を指定
                #     q='ダイエット',
                #     # 表示件数
                #     maxResults=3,
                #     # 視聴回数が多い順に取得
                #     order='viewCount',
                #     type='video',
                # ).execute()
                #
                # youtube_records = search_response['items']


            # レストラン検索APIのURL
            Url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
            # パラメータの設定
            params = {}
            params['keyid'] = settings.GNAVI_API_KEY
            params['hit_per_page'] = 1
            params['shop_name'] = '焼き鳥'
            params['sort'] = 1

            Url = 'https://api.gnavi.co.jp/PhotoSearchAPI/v3/'
            # result_api = requests.get(Url, params)
            # result_api = result_api.json()
            # gnavi_records2 = result_api['response']['0']['photo']

            # gnavi_records2 = result_api['response']


            return render(request, 'robot_app/wants.html', {
                'nav_menu': '何をしたいですか？',
                'gurunavi_search': '1. ぐるなびで検索する',
                'youtube_search': '2. Youtubeで検索する',
                'add_questions': '3. 質問に答える',
                'morning': '4. 朝のやることリスト',
                'type': question_type,
                'mesg': question_mesg,
                'tenki_api': tenki_api,
                'gnavi_records': gnavi_records,
                'carsensor_records': carsensor_records,
                'car_news': car_news,
                'add_car_news': add_car_news,
                'carsensor_records_ver2': carsensor_records_ver2,
                'user': user,
                'weight_result': weight_result,
                'weight': weight,
                'suitable_weight': suitable_weight,
                'overweight': overweight,
                'overweight_text': overweight_text,
                # 'youtube_records': youtube_records,
                # 'gnavi_records2': gnavi_records2,
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
    todo_morning = User_Question.objects.filter(question='todo_morning', user_name=request.user)[0:3]


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


#検索を途中で止めるとinfoのデータが残りエラーになるバグ
info= []
def g_navi(request):
    question_type = ''
    question_mesg = ''
    live = ''
    test_name = ''
    city = ''
    freeword = ''
    name = ''
    image = ''
    url = ''
    address = ''
    result_api = ''
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
            question_mesg = '検索キーワードを入力してください'
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
        'gnavi_records': gnavi_records
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
    weight = ''
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


    return render(request, 'robot_app/morning.html', {
        'wake_up': wake_up,
        'going_work': going_work,
        'nearest_station': nearest_station,
        'arrival_station': arrival_station,
        'todo_morning': todo_morning,
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