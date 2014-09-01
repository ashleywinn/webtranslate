import os.path
from .base import TEST_RESOURCES
from django.test import TestCase
from putonghua.cedict import upload_cedict_file
from putonghua.models import Character, ChinesePhrase, ChineseWord, ChineseName


class CedictUploadTest(TestCase):
    
    def setUp(self):
        cedict_sample_file_1 = os.path.join(TEST_RESOURCES, 'sample_set_1_cedict.txt')
        upload_cedict_file(cedict_sample_file_1)


    def test_can_lookup_phrase(self):
        phrase = ChinesePhrase.objects.get(simplified='林区')
        self.assertIn('region of forest', [eng for eng in phrase.english_list()])

    def test_can_lookup_word(self):
        word = ChineseWord.objects.get_simplified_exact('暴雨')
        self.assertIn('rainstorm', [eng for eng in word.english_list()])
        self.assertIn('阵', word.classifiers)
        self.assertIn('场', word.classifiers)

        word = ChineseWord.objects.get_simplified_exact('桶')
        self.assertIn('bucket', [eng for eng in word.english_list()])
        self.assertIn('只', word.classifiers)


    def test_can_lookup_name(self):
        name = ChineseName.objects.get_simplified_exact('梁辰鱼')
        definition = [eng for eng in name.english_list()][0]
        self.assertRegex(definition, 'Ming dramatist')

        name = ChineseName.objects.get_simplified_exact('林')
        self.assertIn('surname Lin', name.english_list())
        self.assertNotIn('woods', name.english_list())

        word = ChineseWord.objects.get_simplified_exact('林')
        self.assertNotIn('surname Lin', word.english_list())
        self.assertIn('woods', word.english_list())

