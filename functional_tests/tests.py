import sys
from django.contrib.staticfiles.testing import StaticLiveServerCase
from django.utils.encoding import iri_to_uri
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(StaticLiveServerCase):
    fixtures = ['five_hundred_chars.json',]

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()


    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_view_list_of_hsk_words(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('HSK Words').click()
        table = self.browser.find_element_by_id('id_word_list')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('如果',      [row.text for row in rows])
        self.assertIn('if',       [row.text for row in rows])
        self.assertIn('ru2 guo3', [row.text for row in rows])
        

    def test_can_enter_chinese_text_and_retrieve_it_later(self):
        # Steve goes to check out a new translation website
        self.browser.get(self.server_url)

        # Its called Translation Builder
        assert 'Translation Builder' in self.browser.title

        # There is a text box for entering a chinese phrase
        input_instruction = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Enter a sentence or phrase in Chinese', input_instruction)
        input_box = self.browser.find_element_by_id('id_new_phrase')
        self.assertEqual(input_box.get_attribute('placeholder'), '普通话')

        # Steve enters a phrase he'd like to translate
        chinese_phrase = '我会说一点中文'  # '我会说一点普通话'
        input_box.send_keys(chinese_phrase)
        input_box.send_keys(Keys.ENTER)

        # After he hits Enter, he is taken to a new URL for his phrase/sentence
        phrase_url = self.browser.current_url
        self.assertRegex(phrase_url, iri_to_uri('/putonghua/{}/english/'.format(chinese_phrase)))

        # After the phrase is entered definitions are shown for the characters and words
        # and a new text box appears for the user to enter their translation
        table = self.browser.find_element_by_id('id_definitions_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('说', [row.text for row in rows])
        self.assertIn('shuo1', [row.text for row in rows])
        self.assertIn('to say', [row.text for row in rows])
        self.assertIn('一', [row.text for row in rows])
        self.assertIn('yi1', [row.text for row in rows])
        self.assertIn('one', [row.text for row in rows])

        # The input is then re-printed, Chinese above the English with 
        # check boxes next to each character and word

        # The user then marks the Chinese characters and the corresponding English and hits submit


    def test_layout_and_styling(self):
        # Steve's looks more closely at home page design
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_phrase')
        self.assertAlmostEqual((inputbox.location['x'] + 
                                inputbox.size['width'] / 2), 512, delta=5)

        # He does a definition lookup and finds things centered there too
        inputbox.send_keys('你好')
        inputbox.send_keys(Keys.ENTER)

        inputbox = self.browser.find_element_by_id('id_new_english')
        self.assertAlmostEqual((inputbox.location['x'] + 
                                inputbox.size['width'] / 2), 512, delta=5)


                               


if __name__ == '__main__':
    unittest.main(warnings='ignore')


