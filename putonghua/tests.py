from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import iri_to_uri
from putonghua.views import home_page
from putonghua.models import Sentence, ChinesePhrase, EnglishTranslation
from putonghua.models import ChineseCharacter
from putonghua.dictionary import load_cedict_file
from putonghua.dictionary import get_phrase_pinyin
import re

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        

class NewSentenceTest(TestCase):
    
#    def test_saving_a_POST_request(self):
#        self.client.post('/putonghua/new_chinese',
#                         data={'new_phrase': '什么'}
#                         )
#        
#        self.assertEqual(ChinesePhrase.objects.count(), 1)
#        new_sentence = ChinesePhrase.objects.first()
#        self.assertEqual(new_sentence.simplified, '什么')

    def test_redirects_after_POST(self):
        response = self.client.post('/putonghua/new_chinese',
                                    data={'new_phrase': '你好'}
                                    )
        self.assertRedirects(response, iri_to_uri('/english/你好/'))
        
        # self.assertIn('[shen2]', response.content.decode())
        # self.assertIn('what', response.content.decode())


class TranslationViewTest(TestCase):
    fixtures = ['my_test_data.json',]
    
    def test_english_view_displays_components(self):
        response = self.client.get('/english/第二项/')
        self.assertContains(response, 'two')

        response = self.client.get('/english/在我的创作生活中，几乎没有真正的早晨。/')
        self.assertContains(response, 'zhong')


class NewTranslationTest(TestCase):

    def post_new_translation(self, chinese, english):
        return self.client.post('/english/{}/new_translation'.format(chinese),
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
        self.assertRedirects(response, iri_to_uri('/english/你好/'))

class DictionaryModelTest(TestCase):
    fixtures = ['chinese_characters.json',]
#    def setUp(self):
#        load_cedict_file('putonghua/cedict_1_0_ts_utf-8_mdbg.txt')

    def test_can_look_up_pinyin_for_phrase(self):
        pinyin = get_phrase_pinyin('你多大了')
        self.assertIn('ni3', pinyin)
        self.assertIn('duo1', pinyin)
        self.assertIn('da4', pinyin)
        self.assertIn('le5', pinyin)

    def test_can_look_up_characters(self):
        words = ChineseCharacter.objects.filter(simplified='事')
        self.assertIn('affair', [translation.english 
                               for word in words 
                               for translation in word.translations.all()])
        words = ChineseCharacter.objects.filter(simplified='假')
        self.assertIn('to borrow', [translation.english 
                               for word in words 
                               for translation in word.translations.all()])

    
#    def test_can_look_up_definitons(self):
#        words = ChinesePhrase.objects.filter(simplified='事假')
#        self.assertIn('leave of absence', [translation.english 
#                               for word in words 
#                               for translation in word.translations.all()])

