import os
from django.conf import settings
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import iri_to_uri
from putonghua.views import home_page
from putonghua.models import Character, ChinesePhrase
from putonghua.models import ChineseWord, ChineseHskWord

from putonghua.dictionary import upload_hsk_list_file
from putonghua.dictionary import get_phrase_pinyin
import re

TEST_RESOURCES = os.path.abspath(os.path.join(settings.BASE_DIR, 'putonghua/test_resources'))

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        

class NewChineseSentenceTest(TestCase):
    def test_redirects_after_POST(self):
        response = self.client.post('/putonghua/new_chinese',
                                    data={'new_phrase': '你好'}
                                    )
        self.assertRedirects(response, iri_to_uri('/putonghua/你好/english/'))
        

# class TranslationViewTest(TestCase):
#    fixtures = ['my_test_data.json', 'simplified_characters.json']
#    
#    def test_english_view_displays_components(self):
#        response = self.client.get('/putonghua/第二项/english/')
#        self.assertContains(response, 'two')
#
#        response = self.client.get('/putonghua/在我的创作生活中，几乎没有真正的早晨。/english/')
#        self.assertContains(response, 'zhong')


class NewTranslationTest(TestCase):

    def post_new_translation(self, chinese, english):
        return self.client.post('/putonghua/{}/new_translation'.format(chinese),
                                data={'english': english}
                                )
    
    def test_saving_a_POST_request(self):
        self.post_new_translation('什么', 'what?')
        self.assertEqual(ChinesePhrase.objects.count(), 1)
        new_sentence = ChinesePhrase.objects.first()
        self.assertEqual( '什么', new_sentence.simplified)
        self.assertIn('what?', new_sentence.english_list(),)

    def test_redirects_after_POST(self):
        response = self.post_new_translation('你好', 'hi')
        self.assertRedirects(response, iri_to_uri('/putonghua/你好/english/'))


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


class DictionaryModelTest(TestCase):
    fixtures = ['fifteen_chars_phrases.json']
#    fixtures = ['simplified_characters.json']

#    def test_what_characters_and_phrases(self):
#        print("chars: " + 
#              ' '.join(char.char for char in Character.objects.all()))
#        print("phrases: " + 
#              ' '.join(phr.simplified for phr in ChinesePhrase.objects.all()))


    def test_can_look_up_pinyin_for_phrase(self):
        pinyin = get_phrase_pinyin('这个我们的')
        self.assertIn('zhe4', pinyin)
        self.assertIn('ge5', pinyin)
        self.assertIn('wo3', pinyin)
        self.assertIn('men5', pinyin) 
        self.assertIn('de5', pinyin) 

    def test_can_look_up_characters(self):
        word = Character.objects.get(char='在')
        self.assertIn('to exist', [translation.english 
                                 for translation in word.translations.all()])
        word = Character.objects.get(char='是')
        self.assertIn('is', [translation.english 
                               for translation in word.translations.all()])

    # moved this here to avoid loading the fixture twice
    def test_english_view_displays_components(self):
        # response = self.client.get('/putonghua/第二项/english/')
        # self.assertContains(response, 'two')

        response = self.client.get('/putonghua/这个可以好/english/')
        self.assertContains(response, 'this')
        self.assertContains(response, 'possible')
        self.assertContains(response, 'good')

    
#    def test_can_look_up_definitons(self):
#        words = ChinesePhrase.objects.filter(simplified='事假')
#        self.assertIn('leave of absence', [translation.english 
#                               for word in words 
#                               for translation in word.translations.all()])

