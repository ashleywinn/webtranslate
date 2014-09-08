from django.test import TestCase
from django.utils.encoding import iri_to_uri
from putonghua.dictionary import upload_hsk_list_file
from putonghua.cedict import upload_cedict_file
from putonghua.models import Character, ChinesePhrase
from putonghua.dictionary import get_phrase_pinyin, get_components_of_phrase
from putonghua.dictionary import get_toneless_pinyin_components
from .base import test_resource_file

class DictionaryModelTest(TestCase):
    fixtures = ['fifteen_chars_phrases.json']

    def setUp(self):
        upload_hsk_list_file(test_resource_file('hsk_example_file_1.txt'),1)
        upload_cedict_file(test_resource_file('sample_set_3_cedict.txt'))

    def test_cedict_file_loaded_properly(self):
        word = ChinesePhrase.objects.get(simplified='希望')
        self.assertIn('to hope', list(word.english_list()))

    def test_can_look_up_pinyin_for_phrase(self):
        pinyin = get_phrase_pinyin('这个我们的')
        self.assertIn('zhe4', pinyin)
        self.assertIn('ge5', pinyin)
        self.assertIn('wo3', pinyin)
        self.assertIn('men5', pinyin) 
        self.assertIn('de5', pinyin) 

    def test_get_toneless_pinyin_components(self):
        ch_chars = "韩正赴上海纽大调研希望培养更多具国际视野创新型人才"
        full_pinyin = "han2 zheng4 fu4 shang4 hai3 niu3 da4 diao4 yan2 xi1 wang4 pei2 yang3 geng4 duo1 ju4 guo2 ji4 shi4 ye3 chuang4 xin1 xing2 ren2 cai2"

        toneless_words = 'hanzheng fu shanghai niu dadiao yan xiwang peiyang geng duo ju guoji shiye chuangxin xing rencai'
        toneless_words = toneless_words.split()
        tonelesspinyin = ''.join(toneless_words)

        self.assertEqual(toneless_words, list(get_toneless_pinyin_components(tonelesspinyin)))
        self.assertEqual('cai', list(get_toneless_pinyin_components('cai'))[0])
        self.assertEqual('laoshi', list(get_toneless_pinyin_components('laoshi'))[0])

    
    def test_get_phrase_components(self):
        phrase_components = ['韩正','赴','上海','纽','大调',
                             '研','希望','培养','更','多','具',
                             '国际','视野','创新','型','人才']
        phrase_chars = ''.join(phrase_components)
        self.assertEqual(phrase_components, list(get_components_of_phrase(phrase_chars)))

        
    

#    def test_can_look_up_definitons(self):
#        words = ChinesePhrase.objects.filter(simplified='事假')
#        self.assertIn('leave of absence', [translation.english 
#                               for word in words 
#                               for translation in word.translations.all()])

