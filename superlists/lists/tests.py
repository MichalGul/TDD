from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') 
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

        # self.assertTrue(response.content.strip().startswith(b'<html>')) # 
        # self.assertIn(b'<title>Listy rzeczy do zrobienia</title>', response.content) # 
        # self.assertTrue(response.content.strip().endswith(b'</html>')) # 


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "Absolutnie pierwszy element listy"
        first_item.list=list_
        first_item.save()

        secon_item = Item()
        secon_item.text = "Drugi element"
        secon_item.list=list_
        secon_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Drugi element')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='Element pierwszy innej listy', list=other_list)
        Item.objects.create(text='Element drugi innej listy', list=other_list)

        # Wykonaj zwykly http request get
        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'Element pierwszy innej listy')
        self.assertNotContains(response, 'Element drugi innej listy')


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):

        self.client.post('/lists/new',
                        data={'item_text': "Nowy element listy", # url querry parameters
                              "data": str([1,2,3])})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "Nowy element listy")

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'Nowy element listy'}
        )
        new_list=List.objects.first()
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        self.assertRedirects(response, f'/lists/{new_list.id}/')


# class ListViewTest(TestCase):
#
#     def test_displays_all_items(self):
#         list_ = List.objects.create()
#         Item.objects.create(text='itemey 1', list=list_)
#         Item.objects.create(text='itemey 2', list=list_)