from django.core.urlresolvers import resolve
from django.test import TestCase
from todo_list.views import home_page
from django.http import HttpRequest

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
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
