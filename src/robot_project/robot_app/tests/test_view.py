from users.models import User
from robot_app.models import User_Question, GNAVI_Question, Youtube_Question, Blog, News, Schedule, Net_Shop, ChatBot
from django.test import TestCase, Client
from django.urls import reverse

class HomePageTest(TestCase):
    # ログインさせて検証
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'robot_app/index.html')

    def test_can_save_a_POST_requset(self):
        postmethod = self.client.post('/', data={'question': '好きな食べ物はなんですか？', 'answer': '焼肉'})
        # 追加されたかどうか
        self.assertEqual(User_Question.objects.count(), 1)
        # 正しく取り出せているかどうか
        question = User_Question.objects.first()
        self.assertEqual(question.question, "好きな食べ物はなんですか？")
        self.assertEqual(question.answer, "焼肉")

    def test_displays_all_lists_items(self):
        # 作成したオブジェクトがhtml表示されているか
        User_Question.objects.create(question='好きな食べ物は何ですか？', answer='焼肉')
        User_Question.objects.create(question='何歳ですか？', answer='焼肉')
        # #detailに表示
        response = self.client.get(reverse('robot_app:detail', kwargs={'pk': 1}))
        self.assertIn('好きな食べ物', response.content.decode())
        self.assertIn('年齢', response.content.decode())

    # ログアウトさせて検証
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get('/')
        # リダイレクトの確認
        self.assertEqual(response.status_code, 302)
        # リダイレクト先のurl
        self.assertEqual(response.url, '/login/?next=/')


class GnaviPageTest(TestCase):
    # ログインさせて検証
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_gnavi_template(self):
        response = self.client.get('/g_navi/')
        self.assertTemplateUsed(response, 'robot_app/g_navi.html')

    def test_can_save_a_POST_requset(self):
        postmethod = self.client.post('/g_navi/', data={'question': '都道府県を入力してください', 'answer': '東京都'})
        # 追加されたかどうか
        self.assertEqual(GNAVI_Question.objects.count(), 1)
        # 正しく取り出せているかどうか
        question = GNAVI_Question.objects.first()
        self.assertEqual(question.question, "都道府県を入力してください")
        self.assertEqual(question.answer, "東京都")

    def test_displays_all_lists_items(self):
        # 作成したオブジェクトがhtml表示されているか
        User_Question.objects.create(question='都道府県を入力してください', answer='東京都')
        User_Question.objects.create(question='キーワードを入力してください', answer='かに料理')
        # #detailに表示
        response = self.client.get(reverse('robot_app:detail', kwargs={'pk': 1}))
        self.assertIn('住所', response.content.decode())
        # self.assertIn('かに料理', response.content.decode())

    # ログアウトさせて検証
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get('/')
        # リダイレクトの確認
        self.assertEqual(response.status_code, 302)
        # リダイレクト先のurl
        self.assertEqual(response.url, '/login/?next=/')


class YoutubePageTest(TestCase):
    # ログインさせて検証
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_youtube_template(self):
        response = self.client.get('/youtube/')
        self.assertTemplateUsed(response, 'robot_app/youtube.html')

    def test_can_save_a_POST_requset(self):
        postmethod = self.client.post('/youtube/', data={'question': 'キーワードを入力してください', 'answer': 'ヒカキン'})
        # 追加されたかどうか
        self.assertEqual(Youtube_Question.objects.count(), 1)
        # 正しく取り出せているかどうか
        question = Youtube_Question.objects.first()
        self.assertEqual(question.question, "キーワードを入力してください")
        self.assertEqual(question.answer, "ヒカキン")

    def test_displays_all_lists_items(self):
        # 作成したオブジェクトがhtml表示されているか
        Youtube_Question.objects.create(question='キーワードを入力してください', answer='ヒカキン')
        # #detailに表示
        response = self.client.get(reverse('robot_app:detail', kwargs={'pk': 1}))
        self.assertIn('Youtube', response.content.decode())

    # ログアウトさせて検証
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get('/')
        # リダイレクトの確認
        self.assertEqual(response.status_code, 302)
        # リダイレクト先のurl
        self.assertEqual(response.url, '/login/?next=/')


class BlogPageTest(TestCase):
    # ログインさせて検証
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_blog_template(self):
        response = self.client.get('/blog_create/')
        self.assertTemplateUsed(response, 'robot_app/blog.html')

    def test_can_save_a_POST_requset(self):
        postmethod = self.client.post('/blog_create/', data={'title': 'タイトル', 'text': '本文'})
        # 追加されたかどうか
        self.assertEqual(Blog.objects.count(), 1)
        # 正しく取り出せているかどうか
        blog = Blog.objects.first()
        self.assertEqual(blog.title, "タイトル")
        self.assertEqual(blog.text, "本文")

    def test_displays_all_lists_items(self):
        # 作成したオブジェクトがhtml表示されているか
        Blog.objects.create(title='タイトル', text='本文')
        # #detailに表示
        response = self.client.get(reverse('robot_app:detail', kwargs={'pk': 1}))
        # self.assertIn('Youtube', response.content.decode())

    # ログアウトさせて検証
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get('/')
        # リダイレクトの確認
        self.assertEqual(response.status_code, 302)
        # リダイレクト先のurl
        self.assertEqual(response.url, '/login/?next=/')


class NewsPageTest(TestCase):
    # ログインさせて検証
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_news_template(self):
        response = self.client.get('/news/')
        self.assertTemplateUsed(response, 'robot_app/news.html')

    def test_can_save_a_POST_requset(self):
        postmethod = self.client.post('/news/', data={'question': 'celebrity', 'answer': 'ヒカキン'})
        # 追加されたかどうか
        self.assertEqual(News.objects.count(), 1)
        # 正しく取り出せているかどうか
        question = News.objects.first()
        self.assertEqual(question.question, "celebrity")
        self.assertEqual(question.answer, "ヒカキン")

    def test_displays_all_lists_items(self):
        # 作成したオブジェクトがhtml表示されているか
        User_Question.objects.create(question='celebrity', answer='ヒカキン')
        User_Question.objects.create(question='どんなカテゴリが好きですか？', answer='エンタメ')
        # #detailに表示
        response = self.client.get(reverse('robot_app:detail', kwargs={'pk': 1}))
        self.assertIn('好きなタレント', response.content.decode())
        self.assertIn('好きなNews', response.content.decode())

    # ログアウトさせて検証
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get('/')
        # リダイレクトの確認
        self.assertEqual(response.status_code, 302)
        # リダイレクト先のurl
        self.assertEqual(response.url, '/login/?next=/')


class SchedulePageTest(TestCase):
    # ログインさせて検証
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_schedule_template(self):
        response = self.client.get('/mycalendar/')
        self.assertTemplateUsed(response, 'robot_app/mycalendar.html')

    def test_can_save_a_POST_requset(self):
        postmethod = self.client.post('/mycalendar/', data={'date': '2020-08-01', 'summary': 'タイトル',
                     'description': '予定の内容', 'start_time': '7:00', 'end_time': '8:00'})
        # 追加されたかどうか
        self.assertEqual(Schedule.objects.count(), 1)
        # 正しく取り出せているかどうか
        schedule = Schedule.objects.first()
        self.assertEqual(schedule.summary, "タイトル")
        self.assertEqual(schedule.description, "予定の内容")

    def test_displays_all_lists_items(self):
        # 作成したオブジェクトがhtml表示されているか
        Schedule.objects.create(date='2020-01-01', summary='タイトル', description='予定の内容', start_time='7:00', end_time='8:00')
        # #detailには表示しない

    # ログアウトさせて検証
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get('/')
        # リダイレクトの確認
        self.assertEqual(response.status_code, 302)
        # リダイレクト先のurl
        self.assertEqual(response.url, '/login/?next=/')


class NetShopPageTest(TestCase):
    # ログインさせて検証
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_home_template(self):
        response = self.client.get('/net_shop/')
        self.assertTemplateUsed(response, 'robot_app/net_shop.html')

    def test_can_save_a_POST_requset(self):
        postmethod = self.client.post('/net_shop/', data={'question': 'want_object', 'answer': '靴'})
        # 追加されたかどうか
        self.assertEqual(Net_Shop.objects.count(), 1)
        # 正しく取り出せているかどうか
        question = Net_Shop.objects.first()
        self.assertEqual(question.question, "want_object")
        self.assertEqual(question.answer, "靴")

    def test_displays_all_lists_items(self):
        # 作成したオブジェクトがhtml表示されているか
        User_Question.objects.create(question='want_object', answer='靴')
        User_Question.objects.create(question='どんなカテゴリが好きですか？', answer='メンズファッション')
        # #detailに表示しない

    # ログアウトさせて検証
    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get('/')
        # リダイレクトの確認
        self.assertEqual(response.status_code, 302)
        # リダイレクト先のurl
        self.assertEqual(response.url, '/login/?next=/')
