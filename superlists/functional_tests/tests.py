from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # Do wczytywania statycznych plików
import sys, os

def prepare_webdriver():
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_drive_binary = r"E:\Downloads\chromedriver.exe"
    return webdriver.Chrome(chrome_drive_binary, chrome_options=options)

class NewVisitorTest(StaticLiveServerTestCase):

    # @classmethod
    # def setUpClass(cls):
    #     for arg in sys.argv:
    #         if 'liveserver' in arg:
    #             cls.server_url = 'http://' + arg.split('=')[1]
    #             return
    #     super().setUpClass()
    #     cls.server_url = cls.live_server_url
    #
    # @classmethod
    # def tearDownClass(cls):
    #     if cls.server_url == cls.live_server_url:
    #         super().tearDownClass()

    def setUp(self):
        self.browser = prepare_webdriver()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrive_it_later(self):
        # Opis scenariusza testu funkcjonalnego

        # Edyta dowiedziała się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia.
        # Postanowiła więc przejść na stronę główną tej aplikacji.
        self.browser.get(self.live_server_url)

        # Zwróciła uwagę, że tytuł strony i nagłówek zawierają słowo Listy.
        self.assertIn("Listy", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Listy', header_text)

        #Wpisywanie rzeczy do zrobienia
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Wpisz rzecz do zrobienia'
        )

        # W polu tekstowym wpisała "Kupić pawie pióra" (hobby Edyty
        # polega na tworzeniu ozdobnych przynęt).
        inputbox.send_keys('Kupić pawie pióra')

        # Po naciśnięciu klawisza Enter strona została uaktualniona i wyświetla
        # "1: Kupić pawie pióra" jako element listy rzeczy do zrobienia.
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table("1: Kupić pawie pióra")

        # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
        # Edyta wpisała "Użyć pawich piór do zrobienia przynęty" (Edyta jest niezwykle skrupulatna).
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
        inputbox.send_keys(Keys.ENTER)

        # # Strona została ponownie uaktualniona i teraz wyświetla dwa elementy na liście rzeczy do zrobienia.
        self.check_for_row_in_list_table("1: Kupić pawie pióra")
        self.check_for_row_in_list_table(
            "2: Użyć pawich piór do zrobienia przynęty")


        # # Edyta była ciekawa, czy witryna zapamięta jej listę. Zwróciła uwagę na
        # # wygenerowany dla niej unikatowy adres URL, obok którego znajduje się
        # # pewien tekst z wyjaśnieniem.
        ## Używamy nowej sesji przeglądarki internetowej, aby mieć pewność, że żadne
        ## informacje dotyczące Edyty nie zostaną ujawnione, na przykład przez cookies. #
        self.browser.quit()
        self.browser = prepare_webdriver()


        #Franek odwiedza stronę główną.
        #Nie znajduje żadnych śladów listy Edyty
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Kupić pawie pióra", page_text)
        self.assertNotIn("zrobienia przynęty", page_text)

        #Franek tworzy nowa liste - nowe elementy
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Kupić mleko")
        inputbox.send_keys(Keys.ENTER)

        #Franek otrzymuje unikatowy adres URL prowadzący do listy
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #Nie ma sladu po liscie Edyty
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("kupić pawie próra", page_text)
        self.assertIn("Kupić mleko", page_text)

        self.fail('Zakończenie testu!')

        # Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.



    def test_layout_and_styling(self):
        # Edyta przeszla na strone glowna
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()
        print(self.browser.get_window_size())
        # self.browser.set_window_size(1024, 768)

        #Zauwazyla elegancko wysrodkowane pole tekstowe
        inputbox = self.browser.find_element_by_id('id_new_item')
        print(inputbox.location)
        print(inputbox.size)
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            self.browser.get_window_size()['width']/3,
            delta=10
        )

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            self.browser.get_window_size()['width']/3,
            delta=10
        )


