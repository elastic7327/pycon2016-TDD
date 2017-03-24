from selenium import webdriver
import unittest


class NewVersinTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_lists_table")
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrive_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get("http://localhost:8000")

        # She notices the apge title and hearder mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        heard_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', heard_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby)
        # is typing fly-fishing lures)

        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys("\n")

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys("\n")

        # When  she hits enter , the page updates, and noew the page lists
        # "1 : Buy peacock feathers" as an item in a to-di list table

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # There is still a text box inviting her to add another item. she
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)

        def test_is_over(self):
            self.fail("Finish the test!! hoooray!!")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
