
import unittest
from unittest import skip

import ipdb as br

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes the home page and accidentally tries to submit

        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The hom page refreshes, and there is an error message saying
        # The list items cannot be blank

        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # Perversely, She now decides to submit a second bland list item
        self.get_item_input_box().send_keys('\n')

        # She receives a similer warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And She can correct it by filling some tet in
        self.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

        self.fail("write me!")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
