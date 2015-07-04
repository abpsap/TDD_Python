from django.core.urlresolvers import resolve
from django.test import TestCase
from todo_list.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        try:
            request = HttpRequest()
        except NameError:
            print ("ERROR:  Error in your request message")

        response = home_page(request)
        print (repr(response.content.strip()))
        expected_html = render_to_string('home.html')
        self.assertTrue(expected_html, response.content.strip().decode)
