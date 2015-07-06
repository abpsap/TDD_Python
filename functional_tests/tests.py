from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import unittest

#class NewVisitortest(unittest.TestCase):
class NewVisitortest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()
        return

    def check_for_row_in_profile_table(self, row_text):
        table = self.browser.find_element_by_id('id_profile_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has head about a cool new online Match Making app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("Match Making", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your Profile', header_text)

        # She is invited to enter her profile item straight away
        inputbox = self.browser.find_element_by_id('id_new_profile')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter your profile info'
        )

        # She types "But peacock feathers" into a text box
        inputbox.send_keys('Looking for a male soulmate')

        # When she hits enter , she will be taken to a new URL and now the page lists
        # "1: Buy peacock feathers' as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        person1_profile_url = self.browser.current_url
        self.assertRegex(person1_profile_url, '/todo_list/.+')

        self.check_for_row_in_profile_table('Looking for a male soulmate')

        import time
        time.sleep(10)

        # There is still a text box inviting her to add another item
        inputbox = self.browser.find_element_by_id('id_new_profile')
        inputbox.send_keys('Preferred age:25-30, Hobby:Reading, Personality:Humor, Height:6.2')
        inputbox.send_keys(Keys.ENTER)

        time.sleep(5)

        # The page updates again and now shows both items on her list
        self.check_for_row_in_profile_table('Looking for a male soulmate')
        self.check_for_row_in_profile_table('Preferred age:25-30, Hobby:Reading, Personality:Humor, Height:6.2')

        #Now a new user person2 comes along to the site

        ##We need a new browser session to make sure that no information
        ## is coming thro from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Person2 visits the home page and there is no trace of person1's info
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Looking for a male soulmate', page_text)
        self.assertNotIn('Preferred age:25-30', page_text)

        # Person2 starts a new profile by entering a new item, He
        # is less interesting
        inputbox = self.browser.find_element_by_id('id_new_profile')
        inputbox.send_keys('Frank: Looking for a female soulmate')
        inputbox.send_keys(Keys.ENTER)

        # person2 gets his own unique URL
        person2_profile_url = self.browser.current_url
        self.assertRegex(person2_profile_url, '/todo_list/.+')
        self.assertNotEqual(person2_profile_url, person1_profile_url)

        # Again there is no trace of person1 profile on person2's page
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Looking for a male soulmate', page_text)
        self.assertIn('Frank: Looking for a female soulmate', page_text)





if (__name__) == "__main__":
    unittest.main(warnings='ignore')


