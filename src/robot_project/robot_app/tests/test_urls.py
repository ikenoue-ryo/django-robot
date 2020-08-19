from django.urls import resolve, reverse
from django.test import TestCase, Client
from users.models import User
from robot_app.models import User_Question
from robot_app.views.views import indexfunc

class HomePageTest(TestCase):
    #ログインさせる
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    # def test_root_url_resolve_to_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, indexfunc)

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

    def test_redirects_after_POST(self):
        #POST後にリダイレクトされるか確認
        response = self.client.post('/', data={'question': '好きなスポーツはなんですか？', 'answer': 'サッカー'})
        self.assertEqual(response.status_code, 302)
        #リダイレクト先が正しいか確認
        self.assertEqual(response['location'], '/')

    def test_displays_all_lits_items(self):
        User_Question.objects.create(question='好きな食べ物は何ですか？', answer='焼肉')
        User_Question.objects.create(question='何歳ですか？', answer='焼肉')
        # #detailに表示
        response = self.client.get(reverse('robot_app:detail', kwargs={'pk': 1}))
        self.assertIn('好きな食べ物', response.content.decode())
        self.assertIn('年齢', response.content.decode())
