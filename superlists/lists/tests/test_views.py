from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
from lists.forms import ItemForm
# Create your tests here.

class HomePageTest(TestCase):
    maxDiff = None
    # 2 redundant tests
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, home_page)
    #
    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = home_page(request)
    #     expected_html = render_to_string('home.html', {'form': ItemForm()})
    #     self.assertMultiLineEqual(response.content.decode(), expected_html)

        # self.assertTrue(response.content.strip().startswith(b'<html>')) # 
        # self.assertIn(b'<title>Listy rzeczy do zrobienia</title>', response.content) # 
        # self.assertTrue(response.content.strip().endswith(b'</html>')) # 

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


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

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'lists/{correct_list.id}/')
        print(f'lists/{correct_list.id}/')
        print(response.context)
        self.assertEqual(response.context['list'], correct_list) # z jakiegoś powodu test nie działa ale funkcjonalności działa


    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': 'Nowy element dla istniejącej listy'}
        )
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element dla istniejącej listy')
        self.assertEqual(new_item.list, correct_list)


    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': 'Nowy element dla istniejącej listy'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/',
            data = {'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("Element nie może być pusty")
        self.assertContains(response, expected_error)


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


    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("Element nie może być pusty")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


# class ListViewTest(TestCase):
#
#     def test_displays_all_items(self):
#         list_ = List.objects.create()
#         Item.objects.create(text='itemey 1', list=list_)
#         Item.objects.create(text='itemey 2', list=list_)