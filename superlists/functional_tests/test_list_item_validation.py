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

        # Po odświeżeniu strony głównej zobaczyła komunikat błędu
        # informujący o niemożliwości utworzenia pustego elementu na liście.

        # Spróbowała ponownie, wpisując dowolny tekst, i wszystko zadziałało.

        # Przekornie po raz drugi spróbowała utworzyć pusty element na liście.

        # Na stronie listy otrzymała ostrzeżenie podobne do wcześniejszego.

        # Element mogła poprawić, wpisując w nim dowolny tekst.
        self.fail('Napisz mnie!')