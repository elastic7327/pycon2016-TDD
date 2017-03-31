from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from django.template.loader import render_to_string

from lists.models import Item, List
from lists.forms import ItemForm

from lists.views import home_page

import ipdb as br


class HomePageTest(TestCase):
    maxDiff = None

    def test_home_pate_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

#    def test_home_page_can_save_a_POST_request(self):
#        request = HttpRequest()
#        request.method = 'POST'
#        request.POST['item_text'] = 'A new list item'
#
#        response = home_page(request)
#
#        self.assertEqual(Item.objects.count(), 1)
#        new_item = Item.objects.first()
#        self.assertEqual(new_item.text, "A new list item")
#
#    def test_home_page_redirects_after_POST(self):
#        request = HttpRequest()
#        request.method = 'POST'
#        request.POST['item_text'] = 'A new list item'
#        response = home_page(request)
#
#        self.assertEqual(response.status_code, 302)
#        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/%d/' % (list_.id))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_users_list_templates(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
                '/lists/%d/' % (correct_list.id,),
                data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
                '/lists/%d/' % (correct_list.id,),
                data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
                '/lists/%d/' % (list_.id,),
                data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
                '/lists/new',
                data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
                '/lists/new',
                data={'item_text': 'A new list them'}
        )

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id))


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
                '/lists/%d/add_item/' % (correct_list.id),
                data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
                '/lists/%d/add_item/' % (correct_list.id),
                data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id))
        self.assertEquals(response.context['list'], correct_list)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = "You can&#39;t have an empty list item"
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)
