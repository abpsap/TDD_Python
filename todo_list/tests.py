from django.core.urlresolvers import resolve
from django.test import TestCase
from todo_list.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from todo_list.models import Item, Profile

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
#        print (repr(response.content.strip()))
        expected_html = render_to_string('home.html')
        self.assertTrue(expected_html, response.content.strip().decode())

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    # def test_home_page_can_save_a_POST_request(self):
    #     try:
    #         request = HttpRequest()
    #     except NameError:
    #         print ("ERROR:  Error in your request message")
    #
    #     request.method = 'POST'
    #     request.POST['item_text'] = 'A new user profile'
    #
    #     response = home_page(request)
    #
    #     self.assertEqual(Item.objects.count(), 1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text, 'A new user profile')
    #
    # def test_home_page_redirects_after_POST(self):
    #     request = HttpRequest()
    #     request.method = 'POST'
    #     request.POST['item_text'] = 'A new user profile'
    #
    #     response = home_page(request)
    #
    #     self.assertEqual(Item.objects.count(), 1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text, 'A new user profile')
    #
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response['location'], '/todo_list/the-only-profile-in-the-world/')


#***    def test_home_page_displays_all_list_items(self):
#        Item.objects.create(text='item 1')
#        Item.objects.create(text='item 2')
#        request = HttpRequest()
#        response = home_page(request)
#        self.assertIn('item 1', response.content.decode())
#        self.assertIn('item 2', response.content.decode())

class ProfileAndItemModelsTest (TestCase):

    def test_saving_and_retrieving_items(self):
        profile_ = Profile()
        profile_.save()
        first_item = Item()
        first_item.text = 'First Profile item'
        first_item.profile = profile_
        first_item.save()

        second_item = Item()
        second_item.text = 'Second Profile item'
        second_item.profile = profile_
        second_item.save()

        saved_profile = Profile.objects.first()
        self.assertEqual(saved_profile, profile_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'First Profile item')
        self.assertEqual(first_saved_item.profile, profile_)
        self.assertEqual(second_saved_item.text, 'Second Profile item')
        self.assertEqual(second_saved_item.profile, profile_)

class ProfileViewTest(TestCase):

    def test_users_profile_template(self):
        profile_ = Profile.objects.create()
        response = self.client.get('/todo_list/%d/' % (profile_.id,))
        self.assertTemplateUsed(response, 'profile.html')

#    def test_displays_all_items(self):
#        profile_ = Profile.objects.create()
#        Item.objects.create(text='First Profile item', profile = profile_)
#        Item.objects.create(text='Second Profile item', profile = profile_)

#        response = self.client.get('/todo_list/the-only-profile-in-the-world/')

#        self.assertContains(response, 'First Profile item')
#        self.assertContains(response, 'Second Profile item')

    def test_displays_only_items_for_that_profile(self):
        correct_profile = Profile.objects.create()
        Item.objects.create(text='Profile 1', profile=correct_profile)
        Item.objects.create(text='Profile 2', profile=correct_profile)
        other_profile = Profile.objects.create()
        Item.objects.create(text='other Profile item 1', profile=correct_profile)
        Item.objects.create(text='other Profile item 2', profile=correct_profile)

        response = self.client.get('/todo_list/%d/' % (correct_profile.id,))

        self.assertContains(response, 'Profile 1')
        self.assertContains(response, 'Profile 2')
        self.assertContains(response, 'other Profile item 1')
        self.assertContains(response, 'other Profile item 2')

    def test_passes_correct_profile_to_template(self):
        other_profile = Profile.objects.create()
        correct_profile = Profile.objects.create()
        response = self.client.get('/todo_list/%d/' % (correct_profile.id,))
        self.assertEqual(response.context['profile'], correct_profile)


# Add new item/attribute to an existing profile
class NewItemTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/todo_list/new',
            data={'item_text': 'A new profile item-attribute'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new profile item-attribute')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/todo_list/new',
            data = {'item_text' : 'A new profile item-attribute'}
        )
        new_profile = Profile.objects.first()
#        self.assertRedirects(response, '/todo_list/the-only-profile-in-the-world/')
        self.assertRedirects(response, '/todo_list/%d/' % (new_profile.id,))

    def test_can_save_a_POST_request_to_an_existing_profile(self):
        other_profile = Profile.objects.create()
        correct_profile = Profile.objects.create()

        self.client.post (
            '/todo_list/%d/add_item' % (correct_profile.id,),
            data = {'item_text': 'A new item-attribute for an existing profile'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item-attribute for an existing profile')
        self.assertEqual(new_item.profile, correct_profile)

    def test_redirects_to_profile_view(self):
        other_profile = Profile.objects.create()
        correct_profile = Profile.objects.create()

        response = self.client.post(
            '/todo_list/%d/add_item' % (correct_profile.id,),
            data={'item_text': 'A new item-attribute for an existing profile'}
        )

        self.assertRedirects(response, '/todo_list/%d/' % (correct_profile.id,))
