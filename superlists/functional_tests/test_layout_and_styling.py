from selenium import webdriver
from .base import FunctionalTest

def prepare_webdriver():
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_drive_binary = r"D:\Download_D\chromedriver.exe"
    return webdriver.Chrome(chrome_drive_binary, chrome_options=options)


class LayoutAndStylingTest(FunctionalTest):

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
            682.5,
            delta=10
        )

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            682.5,
            delta=10
        )
