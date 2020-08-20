from django.urls import resolve
from django.test import TestCase
from robot_app.views.views import indexfunc, detailfunc, updatefunc, signupfunc, loginfunc, Logout, g_navi, youtube, \
    add_questions, morning, morning_edit, blog_create, news, MyCalendar, MonthCalendar, net_shop, shop_detail, \
    robot_review, notify, week_tenki, any_questions, ajax_answer_add


class UrlResolveTests(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        """indexfuncが呼び出されるかを検証"""
        found = resolve('/')
        self.assertEqual(found.func, indexfunc)

    def test_url_resolves_to_detail_view(self):
        """detailfuncが呼び出されるかを検証"""
        found = resolve('/detail/1/')
        self.assertEqual(found.func, detailfunc)

    def test_url_resolves_to_update_view(self):
        """updatefuncが呼び出されるかを検証"""
        found = resolve('/update/1/')
        self.assertEqual(found.func, updatefunc)

    def test_url_resolves_to_signup_view(self):
        """signupfuncが呼び出されるかを検証"""
        found = resolve('/signup/')
        self.assertEqual(found.func, signupfunc)

    def test_url_resolves_to_login_view(self):
        """loginfuncが呼び出されるかを検証"""
        found = resolve('/login/')
        self.assertEqual(found.func, loginfunc)

    # def test_url_resolves_to_logout_view(self):
    #     """logoutが呼び出されるかを検証"""
    #     found = resolve('/logout/')
    #     self.assertEqual(found.func, Logout)

    def test_url_resolves_to_gnavi_view(self):
        """g_naviが呼び出されるかを検証"""
        found = resolve('/g_navi/')
        self.assertEqual(found.func, g_navi)

    def test_url_resolves_to_youtube_view(self):
        """youtubeが呼び出されるかを検証"""
        found = resolve('/youtube/')
        self.assertEqual(found.func, youtube)

    def test_url_resolves_to_add_questions_view(self):
        """add_questionsが呼び出されるかを検証"""
        found = resolve('/add_questions/')
        self.assertEqual(found.func, add_questions)

    def test_url_resolves_to_morning_view(self):
        """morningが呼び出されるかを検証"""
        found = resolve('/morning/')
        self.assertEqual(found.func, morning)

    def test_url_resolves_to_morning_edit_view(self):
        """morning_editが呼び出されるかを検証"""
        found = resolve('/morning/edit/1/')
        self.assertEqual(found.func, morning_edit)

    def test_url_resolves_to_blog_create_view(self):
        """blog_createが呼び出されるかを検証"""
        found = resolve('/blog_create/')
        self.assertEqual(found.func, blog_create)

    def test_url_resolves_to_news_view(self):
        """newsが呼び出されるかを検証"""
        found = resolve('/news/')
        self.assertEqual(found.func, news)

    # def test_url_resolves_to_mycalendar_view(self):
    #     """MyCalendarが呼び出されるかを検証"""
    #     found = resolve('/mycalendar/')
    #     self.assertEqual(found.func, MyCalendar)

    # def test_url_resolves_to_monthcalendar_view(self):
    #     """MonthCalendarが呼び出されるかを検証"""
    #     found = resolve('/month/01/01/')
    #     self.assertEqual(found.func, MonthCalendar)

    def test_url_resolves_to_net_shop_view(self):
        """net_shopが呼び出されるかを検証"""
        found = resolve('/net_shop/')
        self.assertEqual(found.func, net_shop)

    def test_url_resolves_to_net_shop_detail_view(self):
        """shop_detailが呼び出されるかを検証"""
        found = resolve('/shop_detail/abc/')
        self.assertEqual(found.func, shop_detail)

    # def test_url_resolves_to_map_view(self):
    #     """mapが呼び出されるかを検証"""
    #     found = resolve('/map/')
    #     self.assertEqual(found.func, map)

    def test_url_resolves_to_robot_review_view(self):
        """robot_reviewが呼び出されるかを検証"""
        found = resolve('/robot_review/')
        self.assertEqual(found.func, robot_review)

    def test_url_resolves_to_notify_view(self):
        """notifyが呼び出されるかを検証"""
        found = resolve('/notify/')
        self.assertEqual(found.func, notify)

    def test_url_resolves_to_week_tenki_view(self):
        """week_tenkiが呼び出されるかを検証"""
        found = resolve('/week_tenki/')
        self.assertEqual(found.func, week_tenki)

    def test_url_resolves_to_any_questions_view(self):
        """any_questionsが呼び出されるかを検証"""
        found = resolve('/any_questions/')
        self.assertEqual(found.func, any_questions)

    def test_url_resolves_to_ajax_answer_add_view(self):
        """ajax_answer_addが呼び出されるかを検証"""
        found = resolve('/ajax_answer_add/')
        self.assertEqual(found.func, ajax_answer_add)


