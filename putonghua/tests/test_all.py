from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.encoding import iri_to_uri
from putonghua.models import Character, ChinesePhrase
from putonghua.dictionary import get_phrase_pinyin
        

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
        return self.client.post(reverse('new_translation', args=[chinese]),
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
        self.assertRedirects(response, reverse('view_english', args=['你好']))


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

    
#    def test_can_look_up_definitons(self):
#        words = ChinesePhrase.objects.filter(simplified='事假')
#        self.assertIn('leave of absence', [translation.english 
#                               for word in words 
#                               for translation in word.translations.all()])

