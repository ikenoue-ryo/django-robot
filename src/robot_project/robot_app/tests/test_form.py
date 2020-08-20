from django.test import TestCase
from robot_app.forms import ScheduleForm
from robot_app.models import Schedule


class ScheduleFormTest(TestCase):

    def test_valid(self):
        """正常な入力でエラーにならないことを検証"""
        params = dict(user_name='test@gmail.com', date='2020-01-01', summary='予定のテスト', description='予定のテスト本文', start_time='07:00', end_time='08:00')
        schedule = Schedule()
        form = ScheduleForm(params, instance=schedule)
        self.assertTrue(form.is_valid())

    def test_other(self):
        """入力がなければエラーになることを検証"""
        params = dict()
        schedule = Schedule()
        form = ScheduleForm(params, instance=schedule)
        self.assertFalse(form.is_valid())