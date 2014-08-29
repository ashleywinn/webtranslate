from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import iri_to_uri
from putonghua.views import home_page


class ViewsTest(TestCase):

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
        

