from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import iri_to_uri
from .base import test_resource_file
from putonghua.views import home_page
from putonghua.dictionary import upload_hsk_list_file


class ViewsTest(TestCase):
    fixtures = ['fifteen_chars_phrases.json']

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        
    def test_redirects_after_POST(self):
        response = self.client.post('/putonghua/new_chinese',
                                    data={'new_phrase': '你好'}
                                    )
        self.assertRedirects(response, iri_to_uri('/putonghua/你好/english/'))


    def test_english_view_displays_components(self):
        # response = self.client.get('/putonghua/第二项/english/')
        # self.assertContains(response, 'two')

        response = self.client.get('/putonghua/这个可以好/english/')
        self.assertContains(response, 'this')
        self.assertContains(response, 'possible')
        self.assertContains(response, 'good')


    def test_search_pinyin(self):
        upload_hsk_list_file(test_resource_file('hsk_example_file_1.txt'),1)
        upload_hsk_list_file(test_resource_file('hsk_example_file_2.txt'),2)

        lookup = 'ba'
        response = self.client.get('/putonghua/pinyin/search/{}/'.format(lookup))
        self.assertContains(response, '八')
        self.assertContains(response, '把')

        lookup = 'zhaoxiangji'
        response = self.client.get('/putonghua/pinyin/search/{}/'.format(lookup))
        self.assertContains(response, 'camera')

        lookup = 'bataizhaoxiangji'
        response = self.client.get('/putonghua/pinyin/search/{}/'.format(lookup))
        self.assertContains(response, 'camera')
        self.assertContains(response, 'eight')
    
        

