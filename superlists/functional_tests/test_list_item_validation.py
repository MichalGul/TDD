from selenium import webdriver
from .base import FunctionalTest
from unittest import skip

def prepare_webdriver():
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_drive_binary = r"D:\Download_D\chromedriver.exe"
    return webdriver.Chrome(chrome_drive_binary, chrome_options=options)

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edyta przeszła na stronę główną i przypadkowo spróbowała utworzyć
        # pusty element na liście. Nacisnęła klawisz Enter w pustym polu tekstowym.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('\n')
        # Po odświeżeniu strony głównej zobaczyła komunikat błędu
        # informujący o niemożliwości utworzenia pustego elementu na liście.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Element nie może być pusty")

        # Spróbowała ponownie, wpisując dowolny tekst, i wszystko zadziałało.
        self.get_item_input_box().send_keys('Kupić mleko\n')
        self.check_for_row_in_list_table('1: Kupić mleko')
        # Przekornie po raz drugi spróbowała utworzyć pusty element na liście.
        self.get_item_input_box().send_keys('\n')

        # Na stronie listy otrzymała ostrzeżenie podobne do wcześniejszego.
        self.check_for_row_in_list_table('1: Kupić mleko')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Element nie może być pusty")
        # Element mogła poprawić, wpisując w nim dowolny tekst.
        self.get_item_input_box().send_keys('Zrobić herbatę\n')
        self.check_for_row_in_list_table('1: Kupić mleko')
        self.check_for_row_in_list_table('2: Zrobić herbatę')

