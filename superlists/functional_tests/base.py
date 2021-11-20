from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # Do wczytywania statycznych plików
import sys, os


def prepare_webdriver():
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_drive_binary = r"D:\Download_D\chromedriver.exe"
    return webdriver.Chrome(chrome_drive_binary, chrome_options=options)


class FunctionalTest(StaticLiveServerTestCase):
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
        print(staging_server)
        if staging_server:
            self.live_server_url = 'http://' + staging_server
            print(self.live_server_url)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
