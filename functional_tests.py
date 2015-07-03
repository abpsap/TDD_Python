from selenium import webdriver
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
        self.assertIn("To-Do", self.browser.title)
        self.fail()

        # She is invited to enter a to-do item straight away
        # She types "But peacock feathers" into a text box
        # When she hits enter , the page updates and now the page lists
        # "1: Buy peacock feathers' as an item in a to-do list
        # There is still a text box inviting her to add another item
        # The page updates again and now shows both items on her list
        # Edith navigates to another page and comes back to see if her to-do still exists and it does
        # She logs out.


if (__name__) == "__main__":
    unittest.main(warnings='ignore')


