from os.path import join
from .base import TEST_RESOURCES
from django.test import TestCase
from django.core.exceptions import ValidationError
from putonghua.models import EnglishTranslation
from putonghua.models import Character, ChinesePhrase
from putonghua.models import ChineseWord, ChineseHskWord
from putonghua.dictionary import upload_hsk_list_file
from putonghua.cedict import upload_cedict_file


class ModelsTest(TestCase):
    
    def setUp(self):
        upload_cedict_file(join(TEST_RESOURCES, 'sample_set_2_cedict.txt'))
        upload_hsk_list_file(join(TEST_RESOURCES, 'hsk_example_file_1.txt'),1)


    def test_duplicate_definitions_are_invalid(self):
        EnglishTranslation.objects.get_or_create(english='blah')
        with self.assertRaises(ValidationError):
            eng = EnglishTranslation(english='blah')
            eng.full_clean()


    def test_can_look_up_characters(self):
        word = Character.objects.get(char='在')
        self.assertIn('at', list(word.english_list()))
        word = Character.objects.get(char='是')
        self.assertIn('is', list(word.english_list()))

    def test_hsk_definitions_ranked_before_cedict(self):
        word = ChinesePhrase.objects.get(simplified='星期')
        translations = list(word.chinese_english_translations())
        self.assertEqual(translations[0].english, 'week')
        self.assertIn('day of the week', [trans.english for trans in translations])

        word = Character.objects.get(char='请')
        translations = list(word.chinese_english_translations())
        self.assertEqual(translations[0].english, 'please')
        self.assertEqual(translations[1].english, 'invite')
        self.assertEqual(translations[2].english, 'to treat someone to something')
        self.assertIn('to ask', [trans.english for trans in translations])
        self.assertIn('to request', [trans.english for trans in translations])

    def test_word_definitions_before_names(self):
        word = Character.objects.get(char='谏')
        translations = list(word.chinese_english_translations())
        self.assertEqual(translations[-1].english, 'surname Jian')
        self.assertIn('to remonstrate', [trans.english for trans in translations])
        self.assertIn('to admonish', [trans.english for trans in translations])

    def test_word_classifiers(self):
        word = ChineseWord.objects.filter(classifiers__contains='个').first()
        classifier_cnt = len(word.classifiers)
        self.assertTrue(classifier_cnt > 0)
        word.add_classifier('个')
        self.assertEqual(classifier_cnt, len(word.classifiers))

    def test_tonelesspinyin_lookup(self):
        chars = Character.objects.filter_tonelesspinyin_exact('guo')
        self.assertIn('国', [char.char for char in chars])
        self.assertIn('果', [char.char for char in chars])

        phrases = ChinesePhrase.objects.filter_tonelesspinyin_exact('xingqiliu')
        self.assertIn('星期六', [phrase.simplified for phrase in phrases])
