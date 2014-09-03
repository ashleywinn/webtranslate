from .base import FunctionalTest, TEST_RESOURCES
from django.core.management import call_command
from selenium.webdriver.common.keys import Keys
import os


class PinyinLookupTest(FunctionalTest):

    def test_can_lookup_words_by_pinyin(self):

        call_command("load_hsk_list", 
                     os.path.join(TEST_RESOURCES, 'hsk_example_file_1.txt'),
                     list_num=1)

        call_command("load_cedict_file", 
                     os.path.join(TEST_RESOURCES, 'sample_set_2_cedict.txt'))

        self.browser.get(self.server_url)

        search_box = self.browser.find_element_by_id('id_chinese_search_phrase')
        search_box.send_keys('ta')
        search_box.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_word_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('他',   [row.text for row in rows])
        self.assertIn('她',   [row.text for row in rows])

        search_box = self.browser.find_element_by_id('id_chinese_search_phrase')
        search_box.send_keys('duibuqi')
        search_box.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_word_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('sorry',   [row.text for row in rows])



