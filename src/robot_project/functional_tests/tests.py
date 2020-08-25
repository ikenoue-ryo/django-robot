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
        #タイトルに文字列が含まれるかを確認
        self.assertIn('新規登録', self.browser.title)

        #ユーザーにサインインさせる
        inputbox = self.browser.find_element_by_id('id_mail')
        inputbox.send_keys('test38@gmail.com')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_profname')
        inputbox.send_keys('test38')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_pass')
        inputbox.send_keys('test123')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_pass')
        inputbox.send_keys('test123')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # タイトルに文字列が含まれるかを確認
        self.assertIn('ログイン', self.browser.title)

        # ユーザーにログインさせる
        inputbox = self.browser.find_element_by_id('id_mail')
        inputbox.send_keys('test38@gmail.com')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_pass')
        inputbox.send_keys('test123')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


        # タイトルに文字列が含まれるかを確認
        self.assertIn('ロボット', self.browser.title)

        # ログイン後の最初の質問に答える
        inputbox = self.browser.find_element_by_id('id_answer')
        inputbox.send_keys('焼肉')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        inputbox = self.browser.find_element_by_id('id_answer')
        inputbox.send_keys('サッカー')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        inputbox = self.browser.find_element_by_id('id_answer')
        inputbox.send_keys('30')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        inputbox = self.browser.find_element_by_id('id_answer')
        inputbox.send_keys('3')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)


        # ぐるなびのアクセス確認
        inputbox = self.browser.find_element_by_id('autocomplete_search')
        inputbox.send_keys('ぐるなび')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        # タイトルに文字列が含まれるかを確認
        self.assertIn('ぐるなび', self.browser.title)
        inputbox = self.browser.find_element_by_id('autocomplete_search')
        inputbox.send_keys('東京都')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        inputbox = self.browser.find_element_by_id('autocomplete_search')
        inputbox.send_keys('焼肉')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)


        # Homeに戻る
        self.browser.get("http://localhost:8080/")
        # Youtubeのアクセス確認
        inputbox = self.browser.find_element_by_id('autocomplete_search')
        inputbox.send_keys('Youtube')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        # タイトルに文字列が含まれるかを確認
        self.assertIn('Youtube', self.browser.title)
        inputbox = self.browser.find_element_by_id('id_youtube')
        inputbox.send_keys('ヒカキン')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)


        # Homeに戻る
        self.browser.get("http://localhost:8080/")
        # Youtubeのアクセス確認
        inputbox = self.browser.find_element_by_id('autocomplete_search')
        inputbox.send_keys('質問')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        # タイトルに文字列が含まれるかを確認
        self.assertIn('追加の質問', self.browser.title)

        inputbox = self.browser.find_element_by_id('id_question')
        inputbox.send_keys('170')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_question')
        inputbox.send_keys('70')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_question')
        inputbox.send_keys('1')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_question')
        inputbox.send_keys('1')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_question')
        inputbox.send_keys('マセラティ')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)

        self.fail('テスト終了')
