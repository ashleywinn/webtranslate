from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_chinese_text_and_retrieve_it_later(self):
        # Steve goes to check out a new translation website
        self.browser.get('http://localhost:8000')

        # Its called Translation Builder
        assert 'Translation Builder' in self.browser.title

        # There is a text box for entering a chinese phrase

        # After the phrase is entered definitions are shown for the characters and words
        # and a new text box appears for the user to enter their translation

        # The input is then re-printed, Chinese above the English with 
        # check boxes next to each character and word

        # The user then marks the Chinese characters and the corresponding English and hits submit


if __name__ == '__main__':
    unittest.main(warnings='ignore')


