from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import iri_to_uri
from putonghua.views import home_page
from putonghua.models import Character, ChinesePhrase
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


class DictionaryModelTest(TestCase):
    fixtures = ['simplified_characters.json']

    def test_can_look_up_pinyin_for_phrase(self):
        pinyin = get_phrase_pinyin('你多大了')
        self.assertIn('ni3', pinyin)
        self.assertIn('duo1', pinyin)
        self.assertIn('da4', pinyin)
        # don't yet have a good way of getting the best pinyin for a character
        # self.assertIn('le5', pinyin) 

    def test_can_look_up_characters(self):
        word = Character.objects.get(char='事')
        self.assertIn('affair', [translation.english 
                                 for translation in word.translations.all()])
        word = Character.objects.get(char='假')
        self.assertIn('to borrow', [translation.english 
                               for translation in word.translations.all()])

    # moved this here to avoid loading the fixture twice
    def test_english_view_displays_components(self):
        response = self.client.get('/putonghua/第二项/english/')
        self.assertContains(response, 'two')

        response = self.client.get('/putonghua/在我的创作生活中，几乎没有真正的早晨。/english/')
        self.assertContains(response, 'zhong')

    
#    def test_can_look_up_definitons(self):
#        words = ChinesePhrase.objects.filter(simplified='事假')
#        self.assertIn('leave of absence', [translation.english 
#                               for word in words 
#                               for translation in word.translations.all()])

