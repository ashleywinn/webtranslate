import os.path
from .base import TEST_RESOURCES
from django.test import TestCase
from putonghua.models import ChineseWord, ChineseHskWord
from putonghua.dictionary import upload_hsk_list_file


class HskWordsTest(TestCase):
    
    def setUp(self):
        example_file_1 = os.path.join(TEST_RESOURCES, 'hsk_example_file_1.txt')
        example_file_2 = os.path.join(TEST_RESOURCES, 'hsk_example_file_2.txt')
        upload_hsk_list_file(hsk_list_file=example_file_1, list_number=1)
        upload_hsk_list_file(hsk_list_file=example_file_2, list_number=2)

    def test_can_lookup_hsk_words(self):
        word = ChineseWord.objects.get_simplified_exact('做')
        self.assertIn('make', [eng for eng in word.english_list()])
        word = ChineseWord.objects.get_simplified_exact('我们')
        self.assertIn('we', [eng for eng in word.english_list()])

    def test_can_get_hsk_lists(self):
        list1_words = ['谢谢', '下', '大', '工作', '怎么样']
        list2_words = ['啊', '跟', '自己', '电子邮件', '感兴趣']

        word_list = [hsk.chineseword.get_simplified() 
                     for hsk in ChineseHskWord.objects.filter(hsk_list=1)]
        for simp in list1_words:
            self.assertIn(simp, word_list)
        for simp in list2_words:
            self.assertNotIn(simp, word_list)

        word_list = [hsk.chineseword.get_simplified() 
                     for hsk in ChineseHskWord.objects.filter(hsk_list=2)]
        for simp in list2_words:
            self.assertIn(simp, word_list)
        for simp in list1_words:
            self.assertNotIn(simp, word_list)

