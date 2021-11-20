from selenium import webdriver
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


def prepare_webdriver():
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_drive_binary = r"D:\Download_D\chromedriver.exe"
    return webdriver.Chrome(chrome_drive_binary, chrome_options=options)


class NewVisitorTest(FunctionalTest):

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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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

        # self.fail('Zakończenie testu!')

        # Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.
