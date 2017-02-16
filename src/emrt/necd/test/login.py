import unittest

from edw.seleniumtesting.common import BrowserTestCase
from selenium.webdriver.common.keys import Keys

def suite(browser, base_url):
    """Plone login test 
    """
    # setup a new suite
    suite = unittest.TestSuite()

    for name in LoginTestCase.my_tests():
        testcase = LoginTestCase(name, browser, base_url)
        suite.addTest(testcase)
    
    return suite


class LoginTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url + '/login')

    def test_login(self):
        """Plone login test.
        """
        login_name = self.browser.find_element_by_id("__ac_name")
        passwd = self.browser.find_element_by_id("__ac_password")
        
        login_name.send_keys("test.user")
        passwd.send_keys("test")

        self.browser.find_element_by_name("submit").send_keys(Keys.RETURN)

        user_name = self.browser.find_element_by_id("user-name")
 
        self.assertEqual(user_name.text, "Test User")
