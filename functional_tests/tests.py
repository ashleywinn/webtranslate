from django.test import LiveServerTestCase
from django.utils.encoding import iri_to_uri
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):
    fixtures = ['chinese_characters.json',]
#    fixtures = ['my_test_data.json',]

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_chinese_text_and_retrieve_it_later(self):
        # Steve goes to check out a new translation website
        self.browser.get(self.live_server_url)

        # Its called Translation Builder
        assert 'Translation Builder' in self.browser.title

        # There is a text box for entering a chinese phrase
        input_instruction = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Enter a sentence or phrase in Chinese', input_instruction)
        input_box = self.browser.find_element_by_id('id_new_phrase')
        self.assertEqual(input_box.get_attribute('placeholder'), '普通话')

        # Steve enters a phrase he'd like to translate
        input_box.send_keys('我会说一点普通话')
        input_box.send_keys(Keys.ENTER)

        # After he hits Enter, he is taken to a new URL for his phrase/sentence
        phrase_url = self.browser.current_url
        self.assertRegex(phrase_url, iri_to_uri('/english/我会说一点普通话'))

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


if __name__ == '__main__':
    unittest.main(warnings='ignore')


