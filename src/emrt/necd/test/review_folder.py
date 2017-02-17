import unittest

from emrt.necd.test.util import runas
from edw.seleniumtesting.common import BrowserTestCase
from selenium.webdriver.common.keys import Keys

def suite(browser, base_url, extra_args):

    # setup a new suite
    suite = unittest.TestSuite()

    for name in ReviewFolderTestCase.my_tests():
        testcase = ReviewFolderTestCase(name, browser, base_url, extra_args)
        suite.addTest(testcase)
    
    return suite

class ReviewFolderTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)
    
    @runas("admin")
    def test_review_folder(self):
        """Test 'Save Observation' button exists
        """
        self.browser.get(self.url)

        new_obs = self.browser.find_element_by_link_text("New observation")
        self.assertEqual("New observation", new_obs.text)
        
        #import pdb; pdb.set_trace()
        new_obs.click()
        
        save_obs = self.browser.find_element_by_name("form.buttons.save")
        self.assertEqual("Save Observation", save_obs.get_attribute('value'))
