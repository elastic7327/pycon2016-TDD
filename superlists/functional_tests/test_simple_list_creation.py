import ipdb as br

import unittest

from unittest import skip

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrive_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        # self.browser.get("http://localhost:8000")
        self.browser.get(self.server_url)

        # She notices the apge title and hearder mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        heard_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', heard_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby)
        # is typing fly-fishing lures)

        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys("\n")

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys("\n")

        # When  she hits enter , the page updates, and noew the page lists
        # "1 : Buy peacock feathers" as an item in a to-do list table
        edith_list_url = self.browser.current_url
        self.assertRegexpMatches(edith_list_url, '/lists/.+')

        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. she
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)

        # Now a new user , Francis, comes along to the site.
        # We use a new browser session to make sure that no information
        # of Edith's is comming through from cookies etc#

#        self.browser.quit()
#        self.browser = webdriver.Chrome()

        # Franchis visites the home page. There is no sign of Edith's
        # list

#        self.browser.get(self.live_server_url)
#        page_text = self.browser.find_element_by_tag_name('body').text
#        self.assertNotIn('Buy peacock feathers', page_text)
#        self.assertNotIn('make a fly', page_text)
#
#        # Fancis starts a new list by entering a new item. He
#        # is less interesting than Edith . . . .
#
#        inputbox = self.browser.find_element_by_id('id_new_item')
#        inputbox.send_keys('Buy milk')
#        inputbox.send_keys('\n')
#
#        # Francis gets his own unique URL
#        francis_list_url = self.browser.current_url
#        self.assertRegexpMatches(francis_list_url, '/lists/.+')
#        self.assertNotEqual(francis_list_url, edith_list_url)
#
#        # Again, there is no trace of Edith's list
#        page_text = self.browser.find_element_by_tag_name('body').text
#        self.assertNotIn('Buy peacock feathers', page_text)
#        self.assertIn('Buy milk', page_text)
    pass


if __name__ == "__main__":
    unittest.main(warnings="ignore")
