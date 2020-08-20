from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_web_site(self):
        self.browser.get("http://localhost:8080/signup/")
        # self.browser.get(self.live_server_url)
        #タイトルに文字列が含まれるかを確認
        self.assertIn('スマホ専用ロボット', self.browser.title)

        #ユーザーにサインインさせる
        inputbox = self.browser.find_element_by_id('id_mail')
        inputbox.send_keys('test6@gmail.com')
        time.sleep(3)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        inputbox = self.browser.find_element_by_id('id_profname')
        inputbox.send_keys('test6')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        inputbox = self.browser.find_element_by_id('id_pass')
        inputbox.send_keys('test123')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        inputbox = self.browser.find_element_by_id('id_pass')
        inputbox.send_keys('test123')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        self.fail('テスト終了')




