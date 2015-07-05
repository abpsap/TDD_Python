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
        self.assertTrue(expected_html, response.content.strip().decode())

    def test_home_page_can_save_a_POST_request(self):
        try:
            request = HttpRequest()
        except NameError:
            print ("ERROR:  Error in your request message")

        request.method = 'POST'
        request.POST['item_text'] = 'A new user profile'
        response = home_page(request)
        self.assertTrue('A new user profile', response.content.strip().decode())

        expected_html = render_to_string(
            'home.html',
        {'new_item_text': 'A new user profile'}
        )