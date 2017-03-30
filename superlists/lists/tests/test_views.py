from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item, List

import ipdb as br

# from lists.views import home_page


# class HomePageTest(TestCase):
#
#    def test_root_url_resolve_to_home_page_view(self):
#        found = resolve('/')
#        self.assertEqual(found.func, home_page)
#
#    def test_home_page_returns_correct_html(self):
#        request = HttpRequest()
#        response = home_page(request)
#        # expected_html = render_to_string('lists/home.html')
#        # self.assertEqual(response.content.decode(), expected_html)
#
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
#
#    def test_home_page_only_saves_items_when_necessary(self):
#        request = HttpRequest()
#        home_page(request)
#        self.assertEqual(Item.objects.count(), 0)


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
