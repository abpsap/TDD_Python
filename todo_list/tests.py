from django.core.urlresolvers import resolve
from django.test import TestCase
from todo_list.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from todo_list.models import Item

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

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_can_save_a_POST_request(self):
        try:
            request = HttpRequest()
        except NameError:
            print ("ERROR:  Error in your request message")

        request.method = 'POST'
        request.POST['item_text'] = 'A new user profile'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new user profile')

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new user profile'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new user profile')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/todo_list/the-only-profile-in-the-world/')


#***    def test_home_page_displays_all_list_items(self):
#        Item.objects.create(text='item 1')
#        Item.objects.create(text='item 2')
#        request = HttpRequest()
#        response = home_page(request)
#        self.assertIn('item 1', response.content.decode())
#        self.assertIn('item 2', response.content.decode())

class ItemModelTest (TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'First Profile item'
        first_item.save()

        second_item = Item()
        second_item.text = 'List Profile second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0];
        second_saved_item = saved_items[1];
        self.assertEqual(first_saved_item.text, 'First Profile item')
        self.assertEqual(second_saved_item.text, 'List Profile second')

class ListViewTest(TestCase):

    def test_users_list_template(self):
        response = self.client.get('/todo_list/the-only-profile-in-the-world/')
        self.assertTemplateUsed(response, 'profile.html')

    def test_displays_all_items(self):
        Item.objects.create(text='First Profile item')
        Item.objects.create(text='Second Profile item')

        response = self.client.get('/todo_list/the-only-profile-in-the-world/')

        self.assertContains(response, 'First Profile item')
        self.assertContains(response, 'Second Profile item')
