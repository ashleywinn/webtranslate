from .base import FunctionalTest, TEST_RESOURCES
from django.core.management import call_command
from selenium.webdriver.common.keys import Keys
import os


class HskWordListTest(FunctionalTest):

    def test_can_view_list_of_hsk_words(self):

        call_command("load_hsk_list", 
                     os.path.join(TEST_RESOURCES, 'hsk_example_file_1.txt'),
                     list_num=1)

        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('HSK Word Lists').click()

        table = self.browser.find_element_by_id('id_word_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('商店',         [row.text for row in rows])
        self.assertIn('shop',         table.text)
        self.assertIn('shang1 dian4', [row.text for row in rows])



