from django.test import TestCase
from robot_app.models import User_Question


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

