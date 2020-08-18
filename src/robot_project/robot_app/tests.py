from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from .views.views import indexfunc



class FirstPageTest(TestCase):

    #URLマッピングが正確にできているのか
    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, indexfunc)

