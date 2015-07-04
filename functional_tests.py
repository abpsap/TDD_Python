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

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has head about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn("Match Making", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.asertIn('Match Making', header_text)

        # She is invited to enter her profile item straight away
        inputbox = self.browser.find_element_by_id('id_new_profile')
        self.assertEqual(inputbox.get_attribite('placeholder'),
                         'Enter your profile info'
        )

        # She types "But peacock feathers" into a text box
        inputbox.send_keys('I am a female looking for a match')

        # When she hits enter , the page updates and now the page lists
        # "1: Buy peacock feathers' as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_profile_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == 'I am a female looking for a match' for row in rows)
        )
        # There is still a text box inviting her to add another item
        self.fail('Finish the test!')

        # The page updates again and now shows both items on her list
        # Edith navigates to another page and comes back to see if her to-do still exists and it does
        # She logs out.


if (__name__) == "__main__":
    unittest.main(warnings='ignore')


