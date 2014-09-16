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

        call_command("load_subtlex_csv", 
                     os.path.join(TEST_RESOURCES, 'subtlex_char_sample_set_1.csv'),
                     data_type='char')

        self.search_for_chinese_phrase('ta')

        table = self.browser.find_element_by_id('id_word_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('他',   [row.text for row in rows])
        self.assertIn('她',   [row.text for row in rows])

        self.search_for_chinese_phrase('shi')

        self.browser.implicitly_wait(15)

        shi_char_order = ['是','时','实','师','十','市']
        table = self.browser.find_element_by_id('id_word_table')
        rows = table.find_elements_by_tag_name('tr')
        found_chars = []
        for row in rows:
            cells = row.find_elements_by_tag_name('td')
            if len(cells) == 3:
                found_chars.append(cells[0].text)
        self.assertEqual(found_chars, shi_char_order)

        self.search_for_chinese_phrase('duibuqi')

        table = self.browser.find_element_by_id('id_word_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('sorry',   [row.text for row in rows])



