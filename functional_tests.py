from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitortest(unittest.TestCase):

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
        self.browser.get('http://localhost:8000')

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
        inputbox.send_keys('I am looking for a match')

        # When she hits enter , the page updates and now the page lists
        # "1: Buy peacock feathers' as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_profile_table('I am looking for a match')

        import time
        time.sleep(10)

        # There is still a text box inviting her to add another item
        inputbox = self.browser.find_element_by_id('id_new_profile')
        inputbox.send_keys('Preferred age[25-30], Hobby[Reading], Personality[Humor], Height[6.2]')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and now shows both items on her list
        self.check_for_row_in_profile_table('I am looking for a match')
        self.check_for_row_in_profile_table('Preferred age[25-30], Hobby[Reading], Personality[Humor], Height[6.2]')

        # Edith navigates to another page and comes back to see if her to-do still exists and it does
        # She logs out.


if (__name__) == "__main__":
    unittest.main(warnings='ignore')


