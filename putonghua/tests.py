from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import iri_to_uri
from putonghua.views import home_page
from putonghua.models import Sentence, ChinesePhrase, EnglishTranslation
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
    
    def test_saving_a_POST_request(self):
        self.client.post('/putonghua/new_translation',
                         data={'new_phrase': '什么'}
                         )
        
        self.assertEqual(Sentence.objects.count(), 1)
        new_sentence = Sentence.objects.first()
        self.assertEqual(new_sentence.text, '什么')

    def test_redirects_after_POST(self):
        response = self.client.post('/putonghua/new_translation',
                                    data={'new_phrase': '你好'}
                                    )
        self.assertRedirects(response, iri_to_uri('/english/你好/'))
        
        # self.assertIn('[shen2]', response.content.decode())
        # self.assertIn('what', response.content.decode())
    



class SentenceModelTest(TestCase):

    def test_saving_and_retrieving_a_sentence(self):
        first_sentence = Sentence()
        first_sentence.text = '在我的创作生活中，几乎没有真正的早晨。'
        first_sentence.save()

        second_sentence = Sentence()
        second_sentence.text = '第二项'
        second_sentence.save()

        saved_sentences = Sentence.objects.all()
        self.assertEqual(saved_sentences.count(), 2)
        self.assertEqual(saved_sentences[0].text, '在我的创作生活中，几乎没有真正的早晨。')
        self.assertEqual(saved_sentences[1].text, '第二项')


class DictionaryModelTest(TestCase):

    def update_model_from_ccdict_line(self, match):
        traditional = match.group('traditional')
        simplified  = match.group('simplified')
        pinyin      = match.group('pinyin')
        english     = match.group('english')
        definitions = english.split('/')
        try:
            return ChinesePhrase.objects.get(simplified=simplified, pinyin=pinyin)
        except ChinesePhrase.DoesNotExist: pass
        phrase = ChinesePhrase(simplified=simplified, pinyin=pinyin)
        phrase.save()
        for defined in definitions:
            try:
                english_translation = EnglishTranslation.objects.get(english__iexact=defined)
            except EnglishTranslation.DoesNotExist: 
                english_translation = EnglishTranslation(english=defined)
                english_translation.save()
            phrase.translations.add(english_translation)
        return phrase.save()


    def setUp(self):
        count = 0

        chinese_re = re.compile(r"""(?P<traditional>[\w・，○]+)\s+
                                    (?P<simplified>[\w・，○]+)\s+
                                    \[(?P<pinyin>.*)\]\s+
                                    /(?P<english>.*)/""", re.VERBOSE)
        for line in open('putonghua/cedict_1_0_ts_utf-8_mdbg.txt'):
            if line.startswith('#'): continue

            count += 1
            if count > 5000: return

            m = chinese_re.match(line)
            if m is not None:
                self.update_model_from_ccdict_line(m)
            else:
                print("Not matched: {}".format(line))

    
    def test_can_look_up_definitons(self):
        words = ChinesePhrase.objects.filter(simplified='事假')
        self.assertIn('leave of absence', [translation.english 
                               for word in words 
                               for translation in word.translations.all()])
        pass
