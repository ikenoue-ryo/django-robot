from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from robot_app.models import User_Question, GNAVI_Question, Youtube_Question, Robot_Evaluation, \
    Blog, News, Schedule, Net_Shop, ChatBot
from users.models import User

class UserQuestionModelTest(TestCase):

    def test_is_empty(self):
        saved_answer = User_Question.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        first_question = User_Question()
        first_question.question = '犬は好きですか？'
        first_question.answer = 'はい好きです'
        first_question.save()

        second_question = User_Question()
        second_question.question = '猫は好きですか？'
        second_question.answer = 'いいえ嫌いです'
        second_question.save()

        saved_items = User_Question.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.question, '犬は好きですか？')
        self.assertEqual(second_saved_item.question, '猫は好きですか？')


class GNAVI_QuestionModelTest(TestCase):

    def test_is_empty(self):
        saved_answer = GNAVI_Question.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        first_question = GNAVI_Question()
        first_question.question = '都道府県を入力してください1'
        first_question.answer = '東京都'
        first_question.save()

        second_question = GNAVI_Question()
        second_question.question = '都道府県を入力してください2'
        second_question.answer = '北海道'
        second_question.save()

        saved_items = GNAVI_Question.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.question, '都道府県を入力してください1')
        self.assertEqual(second_saved_item.question, '都道府県を入力してください2')


class Youtube_QuestionModelTest(TestCase):

    def test_is_empty(self):
        saved_answer = Youtube_Question.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        first_question = Youtube_Question()
        first_question.question = 'キーワードを入力してください1'
        first_question.answer = 'ヒカキン'
        first_question.save()

        second_question = Youtube_Question()
        second_question.question = 'キーワードを入力してください2'
        second_question.answer = 'はじめしゃちょー'
        second_question.save()

        saved_items = Youtube_Question.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.question, 'キーワードを入力してください1')
        self.assertEqual(second_saved_item.question, 'キーワードを入力してください2')


class Robot_EvaluationModelTest(TestCase):

    #ログインさせる
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_is_empty(self):
        saved_answer = Robot_Evaluation.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        robot_evaluation1 = Robot_Evaluation()
        robot_evaluation1.user_name = self.user
        robot_evaluation1.robot_name = '案内ロボット1'
        robot_evaluation1.score = '3'
        robot_evaluation1.save()

        robot_evaluation2 = Robot_Evaluation()
        robot_evaluation2.user_name = self.user
        robot_evaluation2.robot_name = '案内ロボット2'
        robot_evaluation2.score = '5'
        robot_evaluation2.save()

        saved_review = Robot_Evaluation.objects.all()
        self.assertEqual(saved_review.count(), 2)

        first_saved_review = saved_review[0]
        second_saved_review = saved_review[1]
        self.assertEqual(first_saved_review.robot_name, '案内ロボット1')
        self.assertEqual(second_saved_review.score, 5)


class BlogModelTest(TestCase):

    #ログインさせる
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_is_empty(self):
        saved_answer = Blog.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        blog1 = Blog()
        blog1.user_name = self.user
        blog1.title = 'タイトル１'
        blog1.text = '本文１'
        blog1.save()

        blog2 = Blog()
        blog2.user_name = self.user
        blog2.title = 'タイトル２'
        blog2.text = '本文２'
        blog2.save()

        saved_blog = Blog.objects.all()
        self.assertEqual(saved_blog.count(), 2)

        first_saved_blog = saved_blog[0]
        second_saved_blog = saved_blog[1]
        self.assertEqual(first_saved_blog.title, 'タイトル１')
        self.assertEqual(second_saved_blog.text, '本文２')


class NewsModelTest(TestCase):

    def test_is_empty(self):
        saved_answer = News.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        first_question = News()
        first_question.question = '好きなタレントは誰ですか？'
        first_question.answer = 'ヒカキン'
        first_question.save()

        second_question = News()
        second_question.question = 'どんなカテゴリが好きですか？'
        second_question.answer = 'general'
        second_question.save()

        saved_items = News.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.question, '好きなタレントは誰ですか？')
        self.assertEqual(second_saved_item.question, 'どんなカテゴリが好きですか？')


class ScheduleModelTest(TestCase):

    #ログインさせる
    def setUp(self):
        self.user = User.objects.create_user('test@gmail.com', 'test123')
        self.client = Client()
        self.client.login(email='test@gmail.com', password='test123')

    def test_is_empty(self):
        saved_answer = Schedule.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        first_question = Schedule()
        first_question.user_name = self.user
        first_question.summary = '釣り'
        first_question.description = '友達と釣りに行く'
        first_question.date = '2020-01-01'
        first_question.save()

        second_question = Schedule()
        second_question.user_name = self.user
        second_question.summary = '旅行'
        second_question.description = '旅行に行く'
        second_question.date = '2020-02-01'
        second_question.save()

        saved_items = Schedule.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.summary, '釣り')
        self.assertEqual(second_saved_item.description, '旅行に行く')


class Net_ShopModelTest(TestCase):

    def test_is_empty(self):
        saved_answer = Net_Shop.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        first_question = Net_Shop()
        first_question.question = '何かほしいものはありますか？'
        first_question.answer = '靴'
        first_question.save()

        second_question = Net_Shop()
        second_question.question = 'どんなカテゴリが好きですか？'
        second_question.answer = 'shoes'
        second_question.save()

        saved_items = Net_Shop.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.question, '何かほしいものはありますか？')
        self.assertEqual(second_saved_item.answer, 'shoes')


class ChatBotModelTest(TestCase):

    def test_is_empty(self):
        saved_answer = ChatBot.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        first_question = ChatBot()
        first_question.question = 'ワインは好きですか？'
        first_question.answer = 'はい'
        first_question.save()

        second_question = ChatBot()
        second_question.question = 'ビールは好きですか？'
        second_question.answer = 'ビールが好きです'
        second_question.save()

        saved_items = ChatBot.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.question, 'ワインは好きですか？')
        self.assertEqual(second_saved_item.answer, 'ビールが好きです')


class UserModelTest(TestCase):

    def test_is_empty(self):
        saved_answer = User.objects.all()
        self.assertEqual(saved_answer.count(), 0)

    #内容が保存されているかの検証
    def test_saving_and_retrieving_question(self):
        first_question = User()
        first_question.email = 'test@gmail.com'
        first_question.profname = 'test'
        first_question.save()

        second_question = User()
        second_question.email = 'test2@gmail.com'
        second_question.profname = 'test2'
        second_question.save()

        saved_items = User.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.email, 'test@gmail.com')
        self.assertEqual(second_saved_item.profname, 'test2')