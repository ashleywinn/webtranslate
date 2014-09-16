from .base import FunctionalTest, TEST_RESOURCES
from django.core.management import call_command
from selenium.webdriver.common.keys import Keys
from putonghua.forms import VALID_PINYIN_ERROR


class DefinitionFormValidation(FunctionalTest):

    def test_uploaded_phrase_definition_are_checked(self):
        self.search_for_chinese_phrase('你好')
        pinyin_input = self.browser.find_element_by_id('id_pinyin')
        pinyin_input.send_keys('ni hao')
        pinyin_input.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(2)
        error = self.browser.find_element_by_css_selector('.has-error li')
        self.assertEqual(error.text, VALID_PINYIN_ERROR)



