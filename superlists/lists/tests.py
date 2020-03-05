from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') 
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('Nowy element listy', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'Nowy element listy'}
            )

        self.assertEqual(response.content.decode(), expected_html)

        # self.assertTrue(response.content.strip().startswith(b'<html>')) # 
        # self.assertIn(b'<title>Listy rzeczy do zrobienia</title>', response.content) # 
        # self.assertTrue(response.content.strip().endswith(b'</html>')) # 
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = "Nowy element listy"

        response = home_page(request)

        self.assertIn("Nowy element listy", response.content.decode())

        

# class SmokeTest(TestCase):

#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)

