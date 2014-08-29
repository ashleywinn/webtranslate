from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

        
class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Steve's looks more closely at home page design
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_phrase')
        self.assertAlmostEqual((inputbox.location['x'] + 
                                inputbox.size['width'] / 2), 512, delta=5)

        # He does a definition lookup and finds things centered there too
        inputbox.send_keys('你好')
        inputbox.send_keys(Keys.ENTER)

        self.browser.implicitly_wait(2)

        inputbox = self.browser.find_element_by_id('id_new_english')
        self.assertAlmostEqual(inputbox.location['x'], 275, delta=10)



