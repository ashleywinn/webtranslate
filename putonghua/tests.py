from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from putonghua.views import home_page
from putonghua.models import Sentence

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_only_saves_sentences_when_necessary(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertEqual(Sentence.objects.count(), 0)
        
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_phrase'] = '什么'

        response = home_page(request)

        self.assertEqual(Sentence.objects.count(), 1)
        new_sentence = Sentence.objects.first()
        self.assertEqual(new_sentence.text, '什么')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        
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
